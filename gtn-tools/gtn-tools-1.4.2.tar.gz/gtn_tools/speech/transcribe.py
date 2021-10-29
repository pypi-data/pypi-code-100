"""
Transcribe audio files with Google Cloud.

Some ressources:

Encoding
https://cloud.google.com/speech-to-text/docs/reference/rest/
v1p1beta1/RecognitionConfig#AudioEncoding

output_config
https://cloud.google.com/speech-to-text/docs/reference/rpc/google.cloud.speech.v1p1beta1#google.cloud.speech.v1p1beta1.LongRunningRecognizeRequest

"""
# BASE
from io import BufferedRandom, BufferedReader, StringIO
from pydub import AudioSegment
import wave
import srt
import time

# GOOGLE APIs
from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import InvalidArgument
from google.cloud.speech_v1p1beta1 import RecognizeResponse

# TYPES
from typing import Any, List, Dict, Union
from starlette.datastructures import UploadFile

from gtn_tools.dependencies.google.storage import upload_blob
from gtn_tools.schemas.constants import Status
from gtn_tools.schemas.transcription_schemas import (
    TranscriptionInputFile,
    Transcription,
    TranscriptionOutputFile
)
from gtn_tools.exceptions import (
    InvalidArgumentException,
    InvalidAudioFormatException
)


class TranscriptionClient:
    def __init__(self) -> None:
        self.preprocessed_file: BufferedRandom = None
        self.file_props: Dict[str, Any] = None
        self.filename: str = None
        return None

    def __mp3_to_wav(
        self,
        file: UploadFile
    ) -> Union[BufferedRandom, UploadFile]:
        """Convert .mp3 files to .wav files"""
        if isinstance(file.filename, BufferedReader):
            self.filename = file.filename.name
            file = file.filename
        else:
            self.filename = file.filename
            file = file.file
        if self.filename.split('.')[1] == "mp3":
            sound = AudioSegment.from_file(file, format="mp3")
            return sound.export(format="wav")
        elif self.filename.split('.')[1] == 'wav':
            return file
        else:
            raise InvalidAudioFormatException

    def __stereo_to_mono(self, file: BufferedRandom) -> BufferedRandom:
        """Convert sterio to mono"""
        sound = AudioSegment.from_file(file, format="wav")
        sound = sound.set_channels(1)

        return sound.export(format="wav")

    def __get_properites(
        self,
        file: BufferedRandom,
    ) -> Dict[str, Any]:
        """Return the frame rate and numer of channels"""
        with wave.open(file, "rb") as wave_file:
            frames = wave_file.getnframes()
            frame_rate = wave_file.getframerate()
            channels = wave_file.getnchannels()

        # reset the pointer to the beginning
        file.seek(0)
        return {
            "frame_rate": frame_rate,
            "channels": channels,
            "seconds": round(frames/float(frame_rate), 4),
            "filename": self.filename.split('/')[-1].split('.')[0] + '.wav'
            }

    def __break_sentences(
        self,
        subs,
        alternatives
    ) -> List[srt.Subtitle]:
        """
        Helper for breaking sentences for creating srt format

        Arguments:
        ---------
        alternatives: "alternative"-response of google speech API
        (results.alternatives)
        """
        firstword = True
        charcount = 0
        idx = len(subs) + 1
        content = ""

        for w in alternatives.words:
            if firstword:
                # first word in sentence, record start time
                start_hhmmss = time.strftime('%H:%M:%S', time.gmtime(
                    w.start_time.seconds))
                start_ms = int(w.start_time.microseconds / 1000)
                start = start_hhmmss + "," + str(start_ms)

            charcount += len(w.word)
            content += " " + w.word.strip()

            if ("." in w.word or "!" in w.word or "?" in w.word or
                    ("," in w.word and not firstword)):
                # break sentence at: . ! ? or line length exceeded
                # also break if , and not first word
                end_hhmmss = time.strftime('%H:%M:%S', time.gmtime(
                    w.end_time.seconds))
                end_ms = int(w.end_time.microseconds / 1000)
                end = end_hhmmss + "," + str(end_ms)
                subs.append(srt.Subtitle(index=idx,
                            start=srt.srt_timestamp_to_timedelta(start),
                            end=srt.srt_timestamp_to_timedelta(end),
                            content=srt.make_legal_content(content)))
                firstword = True
                idx += 1
                content = ""
                charcount = 0
            else:
                firstword = False
        return subs

    def _write_srt(
        self,
        response: RecognizeResponse
    ) -> StringIO:
        subs = []
        for result in response.results:
            subs = self.__break_sentences(subs, result.alternatives[0])

        f = StringIO(srt.compose(subs))
        return f

    def preprocess(
        self,
        file: UploadFile,
        lang: str
    ) -> TranscriptionInputFile:
        # FILE PREPROCESSING
        wav_file = self.__mp3_to_wav(file)
        wav_mono = self.__stereo_to_mono(wav_file)
        file_props = self.__get_properites(wav_mono)
        return TranscriptionInputFile(
            file=wav_mono,
            type='wav',
            lang=lang,
            **file_props
            )


class TranscriptionClientGoogle(TranscriptionClient):
    def __init__(self) -> None:
        super().__init__()
        self.sync_client = speech.SpeechClient
        self.async_client = speech.SpeechAsyncClient
        self.uri: str = None
        return None

    def __call_speech_api(
        self,
        gcs_uri: str,
        lang: str,
        frame_rate: int,
        srt: bool = True
    ) -> RecognizeResponse:
        """Transcribes the audio file specified by the gcs_uri."""
        audio = speech.RecognitionAudio(uri=gcs_uri)
        config = speech.RecognitionConfig(
            enable_word_time_offsets=True,
            enable_automatic_punctuation=True,
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=frame_rate,
            language_code=lang,
        )

        try:
            response = self.sync_client().recognize(config=config, audio=audio)
        except InvalidArgument as e:
            raise InvalidArgumentException(400, e)

        return response

    def transcribe_file(
        self,
        gcloud_bucket: str,
        lang: str,
        file: Union[UploadFile, TranscriptionInputFile] = None,
        srt: bool = False
    ) -> Transcription:
        """Processing Transcription Request"""
        # validate input file
        if isinstance(file, UploadFile):
            file = self.preprocess(file, lang)
        elif not isinstance(file, TranscriptionInputFile):
            raise InvalidArgumentException(
                400,
                ("File must be either starlette.UploadFile or "
                 "TranscriptionInputFile (such as returned by the preprocess "
                 "method)")
            )

        transcription = Transcription(
            input_file=file,
            status=Status.NEW
        )

        # Upload file to Google Cloud storage bucket
        self.uri = upload_blob(gcloud_bucket, file)

        # Call google Speech API with request data
        response = self.__call_speech_api(
            gcs_uri=self.uri,
            lang=lang,
            frame_rate=file.frame_rate,
            srt=srt
        )
        # Each result is for a consecutive portion of the audio. Iterate
        # through them to get the transcripts for the entire audio file.
        # retrun as plain text
        transcription.text = []
        for result in response.results:
            transcription.text.append(result.alternatives[0].transcript)

        if srt:
            srt_file = self._write_srt(response)
            filename = self.uri.split('/')[-1][:(
                self.uri.split('/')[-1].rfind('.')
                )] + '.srt'

            transcription.output_file = TranscriptionOutputFile(
                file=srt_file,
                filename=filename,
                type='srt',
                lang=lang
            )

        return transcription
