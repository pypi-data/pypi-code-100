import typing

class SentinelError(Exception):
    message: typing.Optional[str] = None

    def __init__(self, message: typing.Optional[str] = None) -> None:
        super().__init__(message or self.message or '')

class SentinelInitialisationError(SentinelError):
    message: str = 'Sentinels cannot be instantiated'

class SentinelMutationError(SentinelError):
    message: str = 'Sentinels are immutable'
