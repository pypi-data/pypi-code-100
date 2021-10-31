"""
This is a main class for FileLibrary class.
This class includes a lot of useful functions to process different files
"""

import os
import fnmatch
from .exceptions import FileAlreadyExistsException


class FileLibrary(object):

    def __init__(self, script_name):
        if os.path.isdir(script_name) and not script_name.endswith(os.sep):
            script_name += os.sep
        self.script_name = script_name
        self.script_directory = self.get_script_directory()

    def get_script_directory(self):
        return os.path.abspath(os.path.dirname(self.script_name))

    def rename_file_by_mask(self,
                            is_walk=False,
                            mask_source='*',
                            start_number=1,
                            zeros_count=8,
                            prefix='',
                            suffix=''):
        """
        The method renames masked files in directory define by param 'script_directory'.
        The names of files consist from numbers (starting with start_number) with prefix or suffix
        :param is_walk: if True then use os.walk all tree of directories
        :param mask_source: mask of file - sources
        :param start_number:
        :param zeros_count:
        :param prefix:
        :param suffix:
        :return:
        """

        num = start_number
        for root, dirs, files in os.walk(self.script_directory):
            print(f'root is {root}')
            print(f'dirs are {dirs}')
            for file in files:
                if fnmatch.fnmatch(file.lower(), mask_source.lower()):
                    extension = file.split('.')[1]
                    new_name = prefix + str(num).zfill(zeros_count) + suffix + '.' + extension

                    source = os.path.join(root, file)
                    target = os.path.join(root, new_name)

                    print(f'{source} -> {target}')
                    if os.path.exists(target):
                        raise FileAlreadyExistsException(target)
                    os.rename(source, target)
                    num += 1

            if not is_walk:
                break
