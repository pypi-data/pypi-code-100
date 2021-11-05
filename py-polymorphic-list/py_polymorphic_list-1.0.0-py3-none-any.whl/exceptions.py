class ListIsEmptyError(Exception):
    def __init__(self, message="List is empty!", errors=None):
        super().__init__(message)
        self.errors = errors
