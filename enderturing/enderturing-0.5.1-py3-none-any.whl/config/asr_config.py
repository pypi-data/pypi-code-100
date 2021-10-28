import os

from dataclasses import dataclass

from enderturing.config.config_utils import _init_config_from_url


ENV_ET_ASR_URL = "ET_ASR_URL"
ENV_ET_ASR_SAMPLE_RATE = "ET_ASR_SAMPLE_RATE"


@dataclass
class AsrConfig:
    """Configuration for :class:`enderturing.SpeechRecognizer`.
    Contains settings for speech recognition access.

    Attributes:
        url: URL of an speech recognition instance. Supports "ws" and "wss" schemes.
        sample_rate: ASR instance sample rate. In most cases it's 8000, but can be different for some models
        max_ws_queue: Sets max number of buffered packets. Shouldn't be changed unless recommended by tech support.
    """

    url: str = None
    sample_rate: int = 8000
    max_ws_queue: int = 3

    @classmethod
    def from_url(cls, asr_url: str):
        """Creates `AsrConfig` from a URL.

        Args:
            asr_url: URL with all required options. Example:
                wss://local.enderturing.com/api/v1/ws/asr/0jzfA7kF4acTCK0hetoU9mYKgmRoUauS?sample_rate=8000

        Returns:
            Initialized `AsrConfig` instance.
        """
        return _init_config_from_url(AsrConfig(), asr_url, auth_key_attr=None, auth_secret_attr=None)

    @classmethod
    def from_env(cls):
        """Creates `AsrConfig` from environment variables.
        Supported variables:
        - ET_ASR_URL: ASR URL. Can be either just instance URL
          (e.g. wss://local.enderturing.com/api/v1/ws/asr/0jzfA7kF4acTCK0hetoU9mYKgmRo) or can contain other parameters
          (e.g. wss://local.enderturing.com/api/v1/ws/asr/0jzfA7kF4acTCK0hetoU9mYKgmRoUauS?sample_rate=8000).
          If parameters are set in the URL and as a separate variables - separate variables for parameters have higher
          priority.
        - ET_ASR_SAMPLE_RATE: Value of `sample_rate`

        Returns:
            Initialized `AsrConfig` instance.

        Raises:
            ValueError: if `ET_ASR_URL` environment variable is not set
        """
        asr_url = os.getenv(ENV_ET_ASR_URL)
        if not asr_url:
            raise ValueError("Environment variable 'ET_ASR_URL' is not set, can't use AsrConfig.from_env()")
        config = cls.from_url(asr_url)
        asr_sample_rate = os.getenv(ENV_ET_ASR_SAMPLE_RATE)
        if asr_sample_rate:
            config.sample_rate = int(asr_sample_rate)
        return config
