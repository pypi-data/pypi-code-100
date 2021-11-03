#! /usr/bin/env python3

'''
MIT License

Copyright (c) 2021 Mikhail Hyde & Cole Crescas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import logging
import os
import time

class sysLogger:

    def __init__(self, head=False, file=True, console=True):
        
        self.logger  = logging.getLogger(os.environ['BAY_NO'])
        self.head    = head
        self.file    = file
        self.console = console        

        if self.head:
            self._gen_log_head()

    def _gen_log_head(self):
        '''
        Called in high level object, typically a set of
        worker functions, to identify the root of the logger.
        All function calls will reference the log head.
        '''

        self.logName = ''
        self.gen_log_name()
        
        self.logger = logging.getLogger(os.environ['BAY_NO'])
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')

        file_handler = logging.FileHandler(self.logName)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()

        if self.file:
            self.logger.addHandler(file_handler)

        if self.console:
            self.logger.addHandler(stream_handler)

    def gen_log_name(self):
        '''
        Generates Unique Log Name using the Bay Number
        and datetime.
        '''
        self.logName = '%s%s-%s.log' % (os.environ['LOG_PATH'],
                                        os.environ['BAY_NO'],
                                        time.strftime('%m-%d-%Y',
                                        time.localtime()))

    def INFO(self, msg):
        '''
        Logs message with INFO level
        '''
        self.logger.info(msg)

    def WARNING(self, msg):
        '''
        Logs message with WARNING level
        '''
        self.logger.warning(msg)

    def ERROR(self, msg):
        '''
        Logs message with ERROR level
        '''
        self.logger.error(msg)

    def CRITICAL(self, msg):
        '''
        Logs message with CRITICAL level
        '''
        self.logger.critical(msg)

    def EXCEPTION(self, msg):
        '''
        Logs message and captures exception.
        '''
        self.logger.exception(msg)