class MissingEnvironmentVariableError(Exception):
    def __init__(self, msg: str = None, *args, **kwargs):
        super().__init__(f'The ADARA_SDK_CREDENTIALS environment variable does not exist.{" " + str(msg) if msg else ""}', *args, **kwargs)
