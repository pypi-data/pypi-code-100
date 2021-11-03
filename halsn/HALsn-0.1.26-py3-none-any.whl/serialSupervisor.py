#!/usr/bin/env python3

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

import sys
from HALsn.sysLogger import sysLogger
import serial
import serial.serialutil
import time

class serialRoot:

    '''
    Compartmentalizes serial communication commands between master
    and slave components. 

    Two Pulic Methods:
        Command      - Sends a message to a slave
        Query        - Sends a message requesting data and returns
                         the response
        Master Query - Iterates through query hash map and queries
                         entries that are master query enabled

    Help function should be called to generate the object.
    '''

    def __init__(self, device_path, baud, timeout):

        self.logger = sysLogger()

        self.device_path = device_path
        self.baud        = baud
        self.timeout     = timeout

        self._gen_serial_port()

        self.errorCommand = None

        self.close_port()

    def _gen_serial_port(self):
        '''
        Manually set the serial port object.
        '''
        try:
            self.ser_device = serial.Serial(
                self.device_path, baudrate=self.baud, timeout=self.timeout)
        except serial.serialutil.SerialException:
            self.logger.CRITICAL(f'Port [{self.device_path}] cannont be connected.')
            sys.exit()

    def _reset_buffers(self):
        '''
        Resets Input and Output buffers to prevent
        overflow.
        '''
        self.ser_device.reset_input_buffer()
        self.ser_device.reset_output_buffer()

    def _send_msg(self, msg):
        '''
        Writes a message to the serial slave. Reduces funtion
        call.
        '''

        try:
            self._reset_buffers()
            if self.ser_device.isOpen():
                self.ser_device.write(msg.encode())
            else:
                self.logger.ERROR(f'[{self.device_path}] is closed...')
        except serial.SerialException:
            self.logger.CRITICAL(f'[{self.device_path}]Serial Error while Writing...')
            self.close_port()
            sys.exit()

    def _read_msg(self):
        '''
        Reads a message from the serial slave. Returns False
        if nothing is read. Reduces function call.
        '''

        try:
            self._reset_buffers()
            if self.ser_device.isOpen():
                msg = self.ser_device.read_until(b'\r')
                return msg.decode()
            else:
                self.logger.Critical(f'[{self.device_path}] is closed. Cannot Write')
                pass
        except serial.SerialException:
            self.logger.CRITICAL(f'[{self.device_path}]Serial Error while Reading...')
            self.close_port()
            sys.exit()

    def close_port(self):
        '''
        Closes the serial port to the serial device.
        '''
        if self.ser_device.isOpen():
            self.ser_device.close()
            self.logger.INFO(f'[{self.device_path}] Open = {self.ser_device.isOpen()}')

    def open_port(self):
        '''
        Opens the serial port to the serial device.
        '''
        if not self.ser_device.isOpen():
            self.ser_device.open()
            self.logger.INFO(f'[{self.device_path}] Open = {self.ser_device.isOpen()}')

class serialSupervisor(serialRoot):

    '''
    Compartmentalizes serial communication commands between master
    and slave components. 

    Two Pulic Methods:
        Command      - Sends a message to a slave
        Query        - Sends a message requesting data and returns
                         the response
        Master Query - Iterates through query hash map and queries
                         entries that are master query enabled

    Help function should be called to generate the object.
    '''

    def __init__(self, device_path, baud, timeout):

        super().__init__(device_path, baud, timeout)

    def return_commands(self):
        '''
        Returns list of all available commands for
        device. Useful to print out when developing.
        '''
        return self.commands.keys()

    def return_queries(self):
        '''
        Returns list of all available queries for
        device. Useful to print out when developing.
        '''
        return self.queries.keys()

    def command(self, command_id):
        '''
        Sends command to serial slave. Argument should be a
        string.

        command_id refers to a dictionary key that will send
        the appropriate value to the appropriate slave.
        '''
        command = self.commands[command_id]
        self._send_msg(command)
        time.sleep(0.03)

    def query(self, query_id):
        '''
        Sends request command to serial slave and waits for
        a respone. If no response is received after 3
        attempts, an error is thrown and the code will exit.

        ::returns:: A string response.
        '''

        query = self.queries[query_id][0]
        self._send_msg(query)

        return self._read_msg()

    def specific_query(self, queries):
        '''
        Takes a list of query IDs as an argument. Sends each query
        and collects the response. Intended for special cases where
        looking at subsets of data is required.

        ::returns:: List of Strings
        '''

        row = []

        for query in queries:
            query = self.queries[query][0]
            self._send_msg(query)
            row.append(self._read_msg())
        
        return row

    def master_query(self):
        '''
        Queries every option in the relevant query dictionary
        and compiles it into a list. 

        ::returns:: List of Strings
        '''

        row = []

        for query in self.queries.values():
            if query[1] == 1:
                self._send_msg(query[0])
                row.append(self._read_msg())

        return row
