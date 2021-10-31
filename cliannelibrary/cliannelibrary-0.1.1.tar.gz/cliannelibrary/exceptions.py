class FileAlreadyExistsException(Exception):

    def __init__(self, message):
        self.message = f'File {message} exists. It is impossible to rewrite existing file.'
        super().__init__(self.message)