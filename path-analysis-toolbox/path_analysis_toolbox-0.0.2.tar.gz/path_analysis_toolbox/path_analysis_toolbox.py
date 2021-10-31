import os
import re


class PathAnalyser:
    ILLEGAL_SIGNS = '#%&{}\\<>*?/$!\'":@+`|='
    MAX_FILENAME_LENGTH = 255
    PATH_FOLDER_PATTERN = re.compile(r'(?P<dir>.*)(/|\\)(?P<file>.*)')
    PATH_PATTERN = re.compile(r'(?P<dir>.*)(/|\\)(?P<file>.*)\.(?P<extension>.*)')

    @classmethod
    def replace_all_illegal_signs(cls, original: str, replacement: str = ' ') -> str:
        """
        Removes all illegal signs for filename.

        :param original: original text to replace illegal signs
        :param replacement: string to replace illegal signs with
        :return: text with replaced illegal sings
        """
        if replacement in cls.ILLEGAL_SIGNS:
            raise AttributeError(f'Replacement cannot be {replacement}.')
        for val in cls.ILLEGAL_SIGNS:
            original = original.replace(val, replacement)
        return original

    @classmethod
    def directory(cls, path: str) -> str:
        """
        Returns directory of the path
        """
        directory, file, extension = cls.directory_filename_extension(path)
        return directory

    @classmethod
    def filename(cls, path: str) -> str:
        """
        Returns filename or folder name from the given path
        """
        directory, file, extension = cls.directory_filename_extension(path)
        return file

    @classmethod
    def extension(cls, path: str) -> str:
        """
        Returns extension of file from given path. Empty string if directory.
        """
        directory, file, extension = cls.directory_filename_extension(path)
        return extension

    @classmethod
    def directory_filename(cls, path: str) -> (str, str):
        """
        Returns tuple of directory and filename. If no preceding folder directory empty.
        """
        directory, file, extension = cls.directory_filename_extension(path)
        return directory, file

    @classmethod
    def directory_filename_extension(cls, path: str) -> (str, str, str):
        """
        Returns tuple of directory, filename and extension.
        If no preceding folder directory empty.
        If directory extension empty.
        """
        searched = cls.PATH_PATTERN.search(path)
        try:
            return searched.group('dir'), searched.group('file'), searched.group('extension')
        except AttributeError:
            searched = cls.PATH_FOLDER_PATTERN.search(path)
        try:
            return searched.group('dir'), searched.group('file'), ''
        except AttributeError:
            return '', path, ''

    @classmethod
    def is_directory(cls, path: str) -> bool:
        """
        Checks if given path is a directory (doesn't have an extension)
        """
        return cls.extension(path) == ''

    @classmethod
    def is_file_path(cls, path: str) -> bool:
        """
        Checks if given path contains file (is not a directory)
        """
        return cls.extension(path) != ''

    @classmethod
    def does_path_exist(cls, path: str) -> bool:
        """
        Checks if given path exists
        """
        return os.path.exists(path)

    @classmethod
    def __subsequent_directories_recurrent(cls, path: str, result: list[str]) -> list[str]:
        directory = cls.directory(path)
        if directory != '':
            result.append(directory)
            return cls.__subsequent_directories_recurrent(directory, result)
        else:
            return result

    @classmethod
    def get_subsequent_directories(cls, path: str) -> list[str]:
        """
        :return: list of subsequent directories of given path
        """
        result = []
        if cls.is_directory(path):
            result.append(path)
        result = cls.__subsequent_directories_recurrent(path, result)
        return result[::-1]

    @classmethod
    def __create_directory(cls, directory: str) -> None:
        if not cls.is_directory(directory):
            raise AttributeError(f'Given text: "{directory}" is not a directory.')
        if not os.path.exists(directory):
            os.makedirs(directory)

    @classmethod
    def create_directories(cls, *directories) -> None:
        """
        Creates directories even if preceding folders don't exist.

        :param directories: Relative or absolute directories to be created.
        """
        for directory in directories:
            cls.__create_directory(directory)
