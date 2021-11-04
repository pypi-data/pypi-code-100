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

import time
from HALsn.sysLogger import sysLogger

class Routine:

    def __init__(self, freq=1):
        
        self.freq  = freq
        self.perd  = 1 / self.freq
        self.t0    = 0

        self.fncs  = []
        self.args  = []

        self.bfncs = []
        self.bargs = []

        self.validated = True
        self.logger    = sysLogger(file=False)

    def return_functions(self):
        '''
        Shows all STANDARD functions currently
        appended to the self.fncs member
        '''
        return self.fncs

    def return_args(self):
        '''
        Shows all STANDARD arguments currently
        appended to the self.args member
        '''
        return self.args

    def return_bfunctions(self):
        '''
        Shows all BREAK functions currently
        appended to the self.fncs member
        '''
        return self.bfncs

    def return_bargs(self):
        '''
        Shows all BREAK arguments currently
        appended to the self.args member
        '''
        return self.bargs

    def add_functions(self, fncs, args):
        '''
        Add all STANDARD function-argument pairs to the
        object member
        '''
        if type(fncs) == list and type(args) == list:
            if len(fncs) == len(args):
                for fnc in fncs:
                    self.fncs.append(fnc)
                for arg in args:
                    self.args.append(arg)
            else:
                self.logger.ERROR('The function and arguments are not equivalent. Pass \'None\' if the function does not require arguments.')
                self.validated = False
        else:
            self.fncs.append(fncs)
            self.args.append(args)

    def add_break_functions(self, bfncs, bargs):
        '''
        Add all BREAK function-argument pairs to the
        object member
        '''
        if type(bfncs) == list and type(bargs) == list:
            if len(bfncs) == len(bargs):
                for bfnc in bfncs:
                    self.fncs.append(bfnc)
                for barg in bargs:
                    self.args.append(barg)
            else:
                self.logger.ERROR('The function and arguments are not equivalent. Pass \'None\' if the function does not require arguments.')
                self.validated = False
        else:
            self.bfncs.append(bfncs)
            self.bargs.append(bargs)

    def run(self):
        '''
        Checks that the object is configured to run
        a loop with valid break conditions. Exectues
        all STANDARD functions, then all BREAK
        functions. Exits when the break condition is
        met.
        '''
        if self.validated:
            if len(self.bfncs) > 0:
                self.t0 = self._current_time()
                ti = self.t0

                self._run_fncs()

                while True:

                    tf = self._current_time()
                    if self._two_point_decimal(tf - ti) >= self.perd:
                
                        ti = tf

                        self._run_fncs()

                        event = self._run_bfncs()
                        if event:
                            break
                    time.sleep(0.01)
            else:
                self.logger.ERROR('Cannot run loop without a break condition')
    
    def ext_timer(self):
        '''
        Function to keep track of routine timer in
        the case a function wants to recieve the
        time as an arguement.
        
        ::returns:: Float 
        '''
        tf = self._current_time()
        return self._two_point_decimal(tf - self.t0)

    def _current_time(self):
        '''
        Contained time function. Reduces function
        call

        ::returns:: Float
        '''
        return self._two_point_decimal(time.perf_counter())

    def _run_fncs(self):
        '''
        Executes all STANDARD function argument
        pairs in the object member
        '''
        idx = 0
        for fnc in self.fncs:
            fnc(self.args[idx])
            idx += 1

    def _run_bfncs(self):
        '''
        Executes all BREAK function argument
        pairs in the object member
        '''
        idx = 0
        for bfnc in self.bfncs:
            event =  bfnc(self.bargs[idx])
            if event: 
                return True
            idx += 1

    @staticmethod
    def _two_point_decimal(num):
        '''
        Formatting method to return a decimal to
        two decimal places.

        ::returns:: Float
        '''
        return float('{:.2f}'.format(num))

if __name__ == '__main__':
    
    def rand(*args):
        now = int(time.strftime('%H%M',time.localtime()))
        if now >= args[0]:
            return True

    def test_func(*args):
        for arg in args:
            print(arg)

    rout = Routine()
    rout.add_functions(fncs=[test_func], args=[('Hey', 'Hey')])
    rout.add_break_functions(bfncs=rand, bargs=2105)
    rout.routine()
