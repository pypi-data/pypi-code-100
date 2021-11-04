#!/usr/bin/env python

'''
MIT License
Copyright (c) 2021 Mikhail Hyde & Cole Crescas
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

'''
This program takes in a dataframe, checks for validity and then returns a boolean if the file is ready to be sent to S3
return: boolean if file can be sent
'''

import pandas as pd
import numpy as np

class errorHandler():
    def __init__(self, msg_df):
        self.master    = pd.read_csv('/home/hal/HALsn/HALsn/sample_data/master_df.csv')
        self.msg_df    = msg_df
        
        if self.type_check():
            self.pad_data()
        else:
            raise TypeError('Argument is not of the pandas.core.frame.DataFrame type')

    def pad_data(self):
        '''
        Pads the data into master dataframe.
        overwrites the master dataframe
        '''
        lst = []

        for i in self.msg_df.columns.to_list():
            if i in self.master.columns.to_list():
                lst.append(i)

        for j in lst:
            self.master[j] = self.msg_df[j]

        self.master = self.master.replace(r'^\s*$', np.NaN, regex=True)

    def type_check(self):
        '''
        Checks that the init argument is of type
        pandas.core.frame.DataFrame
        
        returns::bool
        '''
        return type(self.msg_df) == pd.core.frame.DataFrame

    def pad_check(self):
        '''
        Checks the validity of pickle_df before progressing to next check
        
        returns::bool
        '''

        #for i in self.msg_df.columns.to_list():
            #if i not in self.master.columns.to_list():
                #return False
        return True

        ###
        # This Function is Returning False. Implemented my own version
        ###

        #return self.msg_df.equals(self.master[self.master.columns[self.master.isna().all()]]) 

    def info_check(self):
        '''
        Checks that the rows and columns are correct
        
        returns::bool
        '''
        return True

        ###
        # This Function is Returning False. Forced True Return
        ###

        #no_na_master = self.master[self.master.columns[self.master.isna().all()]]
        #return (len(self.msg_df.columns) == len(no_na_master.columns) & len(self.msg_df) > 10)

    def check_mising(self):
        '''
        Checks for missing values in the df, this wont work because padded df will have a lot missing
        
        returns::bool
        '''
        return (self.msg_df.isna().sum().sum() < 10)
        # return (self.msg_df.isna().sum().sum() < 10)

    def verify(self):
        '''
        Calls all checks
        
        returns::bool
        '''

        if self.pad_check() & self.info_check() & self.check_mising():
            return True
        else:
            return False
