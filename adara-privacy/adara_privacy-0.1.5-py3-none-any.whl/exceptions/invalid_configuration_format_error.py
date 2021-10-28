class InvalidConfigurationFormatError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__('The file referenced by the ADARA_SDK_CREDENTIALS environment variable is not in a valid JSON format and cannot be read.', *args, **kwargs)
