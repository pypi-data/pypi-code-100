class YankedVersionError(RuntimeError):
    def __init__(self, reason):
        super().__init__(f'Your innotescus version is not supported and must be updated: {reason}')
