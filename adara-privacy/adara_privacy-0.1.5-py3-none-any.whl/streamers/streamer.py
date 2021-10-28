class Streamer():
    """
    Abstract base class to support streaming operations for token transport.
    """

    def __init__(self):
        super().__init__()

    def __enter__(self):
        """
        Supports the "with" syntax
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        Supports the "with" syntax
        """
        return

    def save(self, identity):
        """
        Abstract method for saving tokens to stream.
        """
        raise NotImplementedError('This method cannot be used on the abstract base class.')
