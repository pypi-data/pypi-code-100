class frameworkError(Exception):
    pass


class PlayerPathNotValid(frameworkError):
    def __init__(self, *args, **kwargs):
        pass


class UnableToWriteToIOFile(frameworkError):
    def __init__(self, *args, **kwargs):
        pass


class UndefinedKeyName(frameworkError):
    def __init__(self, *args, **kwargs):
        pass


class ProcessTerminatedExternally(frameworkError):
    def __init__(self, *args, **kwargs):
        pass
