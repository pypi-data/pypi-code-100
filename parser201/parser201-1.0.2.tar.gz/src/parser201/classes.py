# Author: Peter Nardi
# Date: 11/03/21
# License: MIT (terms at the end of this file)

# Title: parser201 - Apache Log Parser

# imports

# Heavy use of regular expressions
import re


class LogParser:

    # ---------------------------------------------------------------------

    def __init__(self, line):

        # Initial check. If the line passed to the initializer is not a string
        # (type == str), then return an empty LogParser object.

        if type(line) != str:
            self.__noneFields()
            return

        # If a valid string is entered, then perform pre-processing. For some
        # lines, an empty field is represented as two quotes back-to-back, like
        # this: "". The regex to pull out agent strings between quotes will
        # incorrectly ignore that field, rather than returning an empty string.
        # Replace "" with "-" to prevent that.

        clean = line.replace('\"\"', '\"-\"')

        # agentStrings: This part of the regex:(?<!\\)\" is a negative
        # lookbehind assertion. It says, "end with a quote mark, unless that
        # quote mark is preceded by an escape character '\'"

        agentStrings = re.findall(r'\"(.+?)(?<!\\)\"', clean)

        # The next one's tricky. We're looking to extract the statuscode and
        # datasize fields. For some entires, the datasize field is '-', but for
        # all entries the returncode field is a reliable integer. If we split
        # the log line on space, then the first purely isnumeric() item in the
        # resulting list should be the returncode. If we capture the index of
        # that code, and take that code and the one next to it from the list,
        # we should have both fields. If the fields are valid integers, then
        # cast to them int; else set them to 0. If any of this fails, then
        # consider that we have a malformed log line and set all the properties
        # to None.

        try:
            L = clean.split(' ')
            i = [j for j in range(len(L)) if L[j].isnumeric()][0]
            codeAndSize = [int(n) if n.isnumeric() else 0 for n in L[i:i+2]]
            # Splitting on '[' returns a list where item [0] contains the first
            # three fields (ipaddress; userid; username), each separated by
            # space.
            first3 = clean.split('[')[0].split()
        except Exception:
            self.__noneFields()
            return

        # Set properties. If any of these fail, then consider that we have a
        # malformed log line and set all the properties to None.

        try:
            self.__ipaddress = first3[0]
            self.__userid = first3[1]
            self.__username = first3[2]
            self.__timestamp = re.search(
                r'\[(.+?)\]', clean).group().strip('[]')
            self.__requestline = agentStrings[0]
            self.__referrer = agentStrings[1]
            self.__useragent = agentStrings[2]
            self.__statuscode = codeAndSize[0]
            self.__datasize = codeAndSize[1]
        except Exception:
            self.__noneFields()

        return

    # ---------------------------------------------------------------------

    # Method to set every field to None, in the event of a corrupted log line.

    def __noneFields(self):

        for property in [p for p in dir(self) if not p.startswith('_')]:
            setattr(self, property, None)
        return

    # ---------------------------------------------------------------------

    # Method for string rendering of a LogParser object

    def __str__(self):

        labels = ['ipaddress', 'userid', 'username', 'timestamp',
                  'requestline', 'statuscode', 'datasize', 'referrer',
                  'useragent']
        padding = len(max(labels, key=len))
        L = []

        # Build the string in the same order as the labels.
        for label in labels:
            L.append(f'{label:>{padding}}: {getattr(self, label)}')

        return '\n'.join(L)

    # ---------------------------------------------------------------------

    # Setters and Getters. Might need to perform input validation at some point
    # in the future.

    # -------------------------------
    # ipaddress property

    @property
    def ipaddress(self):
        return self.__ipaddress

    @ipaddress.setter
    def ipaddress(self, value):
        self.__ipaddress = value

    # -------------------------------
    # userid property

    @property
    def userid(self):
        return self.__userid

    @userid.setter
    def userid(self, value):
        self.__userid = value

    # -------------------------------
    # username property

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    # -------------------------------
    # timestamp property

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, value):
        self.__timestamp = value

    # -------------------------------
    # requestline property

    @property
    def requestline(self):
        return self.__requestline

    @requestline.setter
    def requestline(self, value):
        self.__requestline = value

    # -------------------------------
    # statuscode property

    @property
    def statuscode(self):
        return self.__statuscode

    @statuscode.setter
    def statuscode(self, value):
        self.__statuscode = value

    # -------------------------------
    # datasize property

    @property
    def datasize(self):
        return self.__datasize

    @datasize.setter
    def datasize(self, value):
        self.__datasize = value

    # -------------------------------
    # referrer property

    @property
    def referrer(self):
        return self.__referrer

    @referrer.setter
    def referrer(self, value):
        self.__referrer = value

    # -------------------------------
    # useragent property

    @property
    def useragent(self):
        return self.__useragent

    @useragent.setter
    def useragent(self, value):
        self.__useragent = value

# ---------------------------------------------------------------------


if __name__ == '__main__':  # pragma no cover
    pass

# ---------------------------------------------------------------------

# MIT License
#
# Copyright (c) 2020-2021 Peter Nardi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions: # The above
# copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
