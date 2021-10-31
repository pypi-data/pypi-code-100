class BaseError(Exception):
    """
        Base class for curriculum processing exceptions.
    """

    def __init__(self, message: str, phase: str):
        self.message = message
        self.phase = phase

    def __str__(self):
        s = f"Error: {self.message}, Phase: {self.phase}"
        return s
