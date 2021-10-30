#!/usr/bin/env python
#************************************************************************
# Copyright 2021 O7 Conseils inc (Philippe Gosselin)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#************************************************************************

"""Package to explores files & directories """

import os
#import pprint
import o7lib.util.input
import o7lib.util.displays



#*************************************************
# https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
#*************************************************
class Colors:
    """Constant for Console Colors"""
    HEADER = '\033[5;30;47m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#*************************************************
#
#*************************************************
class FileExplorer():
    """Class to explore files & directories"""

    #*************************************************
    #
    #*************************************************
    def __init__(self, cwd = '.'):

        self.cwd = os.path.realpath(cwd)


    #*************************************************
    #
    #*************************************************
    def ScanDirectory(self):
        """List all files in the current directory """
        files = []

        # https://docs.python.org/3/library/os.html#os.scandir
        with os.scandir(path = self.cwd) as entries:
            for entry in entries:

                # https://docs.python.org/3/library/os.html#os.stat_result
                stats = entry.stat()
                #print(f'{entry.name} - stats: {stats}')

                fType = ''
                size = stats.st_size
                if entry.is_dir():
                    fType += 'd'
                    size = None
                if entry.is_file():
                    fType += 'f'
                if entry.is_symlink():
                    fType += 's'

                files.append({
                    'name': entry.name,
                    'path' : entry.path,
                    'type' : fType,
                    'size' : size,
                    #'created': stats.st_birthtime,
                    'updated' : stats.st_mtime
                })

        # Sort list
        files.sort(key=lambda x: x.get('type') + x.get('name'))


        return files

    #*************************************************
    #
    #*************************************************
    def DiplayDirectory(self):
        """Display the Current Directory"""

        #diskUsage = shutil.disk_usage(self.cwd)
        cwdList = self.ScanDirectory()
        # print('Disk Usage')
        # pprint.pprint(diskUsage)

        # print('list Dir')
        # pprint.pprint(cwdList)
        params = {
            'title' : f'Active Directory: {self.cwd}',
            'columns' : [
                {'title' : 'id'      , 'type': 'i',       'minWidth' : 4  },
                {'title' : 'Type'    , 'type': 'str',  'dataName': 'type'},
                {'title' : 'Name'    , 'type': 'str',  'dataName': 'name'},
                {'title' : 'Size'    , 'type': 'bytes',  'dataName': 'size'},
                {'title' : 'Updated', 'type': 'since', 'dataName': 'updated'}
            ]
        }
        o7lib.util.displays.Table(params, cwdList)

        return cwdList




    #*************************************************
    #
    #*************************************************
    def SelectFile(self):

        while True :
            cwdList = self.DiplayDirectory()
            keyType, key = o7lib.util.input.InputMulti('Option -> Back(b) Select File (int): ')

            if keyType == 'str':
                if key.lower() == 'b':
                    return None

            if keyType == 'int' and key > 0 and key <= len(cwdList):
                print(f'Selected File : {cwdList[key - 1]["path"]}')
                file = cwdList[key - 1]
                if file["type"] == 'd':
                   self.cwd = file['path']
                else:
                    return file['path']


#*************************************************
# To Test Class
#*************************************************
if __name__ == "__main__":


    theFE = FileExplorer(cwd = '.')
    theFE.SelectFile()
