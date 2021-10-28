import logging

from pathlib import Path
from typing import List, Literal, Optional, Union
from urllib.parse import quote, urlencode, urlparse

from enderturing.config import AsrConfig, Config
from enderturing.ffmpeg_helper import _get_ffmpeg_file_cmd, _get_ffmpeg_join_files_cmd
from enderturing.http_client import HttpClient
from enderturing.recognition_stream import RecognitionResultFormat, RecognitionStream


log = logging.getLogger("enderturing")


class SpeechRecognizer:
    """Class to interact with Ender Turing speech recognition instances.
    Contains utility methods to simplify sending different formats of audio files for recognition.
    """

    def __init__(self, config: Optional[AsrConfig] = None, api_config: Optional[Config] = None):
        self.config = config or AsrConfig.from_env()
        self.api_config = api_config
        self._http_client = None

    def _build_server_url(self, **kwargs):
        return self.config.url + "?" + urlencode(kwargs, quote_via=quote)

    def stream_recognize_joined_file(
        self,
        channel_files: List[Union[str, Path]],
        *,
        result_format: Union[str, RecognitionResultFormat] = RecognitionResultFormat.jsonl,
        include_partials: bool = False,
        extra_ws_params: dict = None,
    ):
        """Sends multichannel audio for recognition when each channel is a separate audio file.
        For example some contact center software generates two files per call: one for a client and one
        for a support agent. But for analysis it's preferable to see transcripts of the files merged as a dialog.

        Args:
            channel_files: List of files to treat as channels. In most scenarios you have two files for stereo.
            result_format: Defines whether to return a plain text or structured data with meta information.
                 For 'jsonl' format a json object per line is returned.
            include_partials: Defines whether to return partially-recognized utterances. Only works with 'jsonl'.
                 If `True` - results would include objects like `{"partial": "hello wo"}`. Otherwise only fully
                 recognized utterances would be included.
            extra_ws_params: Send specific params to ASR.

        Returns:
            An async text file-like object. See :class:`enderturing.RecognitionStream`
        """
        src_files = [Path(x) for x in channel_files]
        cmd, asr_channels = _get_ffmpeg_join_files_cmd(src_files, asr_sample_rate=self.config.sample_rate)
        res_format = result_format
        if isinstance(res_format, str):
            res_format = RecognitionResultFormat[res_format]
        asr_url = self._build_server_url(source="FILE", file_path=src_files[0].name)
        return RecognitionStream(
            asr_url=asr_url,
            cmd=cmd,
            src_file=src_files[0],
            asr_channels=asr_channels,
            sample_rate=self.config.sample_rate,
            res_format=res_format,
            extra_ws_params=extra_ws_params or {},
            include_partials=include_partials,
            max_ws_queue=self.config.max_ws_queue,
        )

    def stream_recognize(
        self,
        path: Union[str, Path],
        *,
        channels: Union[List[int], int, Literal["all", "mono"]] = "all",
        result_format: Union[Literal["text", "jsonl"], RecognitionResultFormat] = RecognitionResultFormat.jsonl,
        include_partials: bool = False,
        extra_ws_params: dict = None,
    ) -> RecognitionStream:
        """Sends specified audio file to speech recognition.

        Args:
            path: Path to audio file for recognition.
            channels: Specifies which audio channels to send for recognition.
                Supported values:
                - "all" (default) - recognizes all detected audio channels, e.g. 1 if it's a mono file, 2 for stereo
                - "mono" - mixes all channels to a single channel. Useful when recording is done in stereo format for
                  a single speaker
                - int - number of channels for recognition. E.g. if channels=1 for stereo - only first channel
                  would be recognized.
                - list[int] - enumeration of channels for recognition, indices are zero-based. E.g. if channels=[1]
                  for a stereo file - only second channel would be recognized
            result_format: Defines whether to return a plain text or structured data with meta information.
                 For 'jsonl' format a json object per line is returned.
            include_partials: Defines whether to return partially-recognized utterances. Only works with 'jsonl'.
                 If `True` - results would include objects like `{"partial": "hello wo"}`. Otherwise only fully
                 recognized utterances would be included.
            extra_ws_params: Send specific params to ASR.

        Returns:
            An async text file-like object. See :class:`enderturing.RecognitionStream`
        """
        src_file = path if isinstance(path, Path) else Path(path)
        cmd, asr_channels = _get_ffmpeg_file_cmd(src_file, self.config.sample_rate, channels)
        res_format = result_format
        if isinstance(res_format, str):
            res_format = RecognitionResultFormat[res_format]
        asr_url = self._build_server_url(source="FILE", file_path=src_file.name)
        return RecognitionStream(
            asr_url=asr_url,
            cmd=cmd,
            src_file=src_file,
            asr_channels=asr_channels,
            sample_rate=self.config.sample_rate,
            res_format=res_format,
            extra_ws_params=extra_ws_params or {},
            include_partials=include_partials,
            max_ws_queue=self.config.max_ws_queue,
        )

    def _recognize_file(
        self,
        path: Union[str, Path],
        *,
        channels: Union[List[int], int, Literal["all", "mono"]] = "all",  # TODO
        result_format: Union[Literal["text", "jsonl"], RecognitionResultFormat] = RecognitionResultFormat.text,
        realtime: bool = False,
        api_config: Optional[Config] = None,
    ) -> dict:
        """
        Recognize file using API POST method.
        Can provide recognition results for files up to 30 seconds by flag 'realtime'

        Args:
            path: Path to audio file for recognition.
            channels: Specifies which audio channels to send for recognition.
                Supported values:
                - "all" (default) - recognizes all detected audio channels, e.g. 1 if it's a mono file, 2 for stereo
                - "mono" - mixes all channels to a single channel. Useful when recording is done in stereo format for
                  a single speaker
                - int - number of channels for recognition. E.g. if channels=1 for stereo - only first channel
                  would be recognized.
                - list[int] - enumeration of channels for recognition, indices are zero-based. E.g. if channels=[1]
                  for a stereo file - only second channel would be recognized
            result_format: Defines whether to return a plain text or structured data with meta information.
                 For 'jsonl' format a json object per line is returned.
            realtime: Defines whether to return recognized results back or just provide session_id to read through API.
                 If `True` - recognized results would be returned in addition to meta-data dictionary.
            api_config: settings for API access.

        Returns:
            A dictionary containing session_id, and results (in text or raw json format).

        Raises:
            ValueError: If no api_config provided
        """
        res_format = result_format
        if isinstance(res_format, str):
            res_format = RecognitionResultFormat[res_format]

        api_config = api_config or self.api_config
        if not api_config:
            raise ValueError("API config has to be set either in constructor or as argument")

        if isinstance(path, Path):
            path = str(path)

        parsed_path = urlparse(path)

        asr_token = self.config.url.split("/")[-1]
        params = dict(
            token=asr_token,
            caller_id=path,
            realtime=realtime,
            detailed_realtime_results=True if res_format is RecognitionResultFormat.jsonl else False,
        )
        if not self._http_client:
            # TODO instance per API config
            self._http_client = HttpClient(api_config)

        if parsed_path.scheme == "et":
            params["filename"] = parsed_path.path
            return self._http_client.post("/recognizer/local-audio-file", params=params)

        return self._http_client.post("/recognizer/audio-file", params=params, files={"file": open(path, "rb")})

    def recognize_file(
        self,
        path: Union[str, Path],
        *,
        result_format: Union[Literal["text", "jsonl"], RecognitionResultFormat] = RecognitionResultFormat.text,
        api_config: Optional[Config] = None,
    ) -> dict:
        """
        Recognize file using API POST method and return recognized result back.
        Can provide recognition results for files up to 30 seconds

        Args:
            path: Path to audio file for recognition.
            result_format: Defines whether to return a plain text or structured data with meta information.
                 For 'jsonl' format a json object per line is returned.
            api_config: settings for API access.

        Returns:
            A dictionary containing session_id, and results (in text or raw json format).
        """
        kwargs = dict(result_format=result_format, api_config=api_config)
        return self._recognize_file(path, realtime=True, **kwargs)

    def recognize_file_long(
        self,
        path: Union[str, Path],
        *,
        api_config: Optional[Config] = None,
    ) -> dict:
        """
        Recognize file using API POST method and return session_id for recognized file.
        No transcripts will be returned.

        Args:
            path: Path to audio file for recognition.
            api_config: settings for API access.

        Returns:
            A dictionary containing session_id to access results through API.
        """
        kwargs = dict(api_config=api_config)
        return self._recognize_file(path, realtime=False, **kwargs)
