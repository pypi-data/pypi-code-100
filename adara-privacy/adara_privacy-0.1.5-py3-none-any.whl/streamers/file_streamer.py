import json
from typing import Union

from adara_privacy.identity import Identity
from adara_privacy.privacy_token import Token
from adara_privacy.streamers.streamer import Streamer
from adara_privacy.utils.strings import is_empty_string


class FileStreamer(Streamer):
    """
    Saves and reads identity tokens to/from disk in a consistent file format.
    """

    def __init__(self, file_name: str, file_format: str = 'token'):
        """
        Creates a new instance of a FileStreamer.

        Args:
            file_name (str): Path and filename (with extension) of token set data file
            file_format (str): Defines whether the file is for data of type "token" or "identity" (default: "token")
        """
        super().__init__()

        self._mode = 'r'

        # validate arg: file_name
        if isinstance(file_name, str) and not is_empty_string(file_name):
            self._filename = file_name
        else:
            raise ValueError('Argument "file_name" must be a non-empty string.')

        # validate arg: file_format
        if isinstance(file_format, str) and file_format.strip().lower() in {'token', 'identity'}:
            self._file_format = file_format.strip().lower()
        else:
            raise ValueError('Argument "file_format" must be either "token" or "identity".')

        # init instance defaults
        self._file = None  # stores the file handle after opening

    def __enter__(self):
        """
        Supports the "with" syntax
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        Supports the "with" syntax
        """
        self.close()
        return

    @property
    def _is_file_open(self) -> bool:
        """
        Private method to return whether a file handle is currently open.

        Returns:
            bool: True if there is an open handle, otherwise False.
        """
        return self._file is not None and not self._file.closed

    def open(self, mode: str = 'read'):
        """
        Opens the file represented by the file_name argument passed to the constructor.

        Args:
            mode (str): Mode for opening the file.  Options are:
                "read" / "r" : opens file for reading only
                "append" / "a" : opens file for appended writes (will not overwrite existing, appends data starting at end of file)
                "write" / "w" : opens file for writing; WARNING: will overwrite any existing file with the same name

                NOTE: Both "append" and "write" modes will create the file if it does not already exist
        """

        if isinstance(mode, str):
            mode = mode.strip().lower()
            if mode in {'read', 'r'}:
                self._mode = 'r'
            elif mode in {'append', 'a'}:
                self._mode = 'a'
            elif mode in {'write', 'w'}:
                self._mode = 'w'
            else:
                raise ValueError('Argument "mode" must be one of "r", "a", or "w".')
        else:
            raise TypeError('Argument "mode" must be one of "r", "a", or "w".')

        # close any currently open handles
        if self._is_file_open:
            self._file.close()

        self._file = open(file=self._filename, mode=self._mode)

    def close(self):
        """
        Closes the file.
        """
        if self._is_file_open:
            self._file.close()

    def save(self, item: Identity):
        """
        Saves tokens to the file. Automatically opens the file if it's not already open.

        Args:
            identity (Identity): An instance of an Identity that contains tokens to write to the file.
        """
        # arg check: item type
        if not isinstance(item, Identity):
            raise TypeError('Argument "item" must be an instance of Identity.')

        # ensure the file is open
        if not self._is_file_open:
            self.open('append')

        # choose the object type to write
        if self._file_format == 'token':
            data = item.to_dict(format='token')
        else:
            data = item.to_dict()

        # write the record in a single line
        # prefix the string with newline if there are previous records
        self._file.write(
            json.dumps(data) + '\n'
        )
        self._records_written = True

    def read(self) -> Identity:
        """
        Reads tokens from the file. Automatically opens the file if it's not already open.
        This is a generator that supports iteration for line-by-line read operations.

        Yields:
            Identity: Returns an instance of an identity containing the tokens read from a single line of the file.
        """
        # ensure the file is open
        if not self._is_file_open:
            self.open('read')

        # read line by line and return instances based on self._file_format
        for line in self._file:
            yield Identity(json.loads(line))
