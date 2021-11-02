'''This is a library about automatic number-taking of "General Chinese Author Number Table". 
   At present, there is only one way to take the number, that is, directly looking up the table.
   In the future, we will adapt to a variety of author numbering methods, please wait.
   
   You can use the distributecode() method or fetchcode() method to find the author number.'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
THIS FILE IS PART OF NETWORK FOR MWAFU LIBRARY LOVE BOOK STORE BY MATT BELFAST BROWN
auto_AUTHNumber.py - The core part of the Author Number library.

Author: Matt Belfast Brown 
Creat Date:2021-05-30
Version:0.14.13

THIS PROGRAM IS FREE FOR EVERYONE,IS LICENSED UNDER GPL-3.0
YOU SHOULD HAVE RECEIVED A COPY OF GPL-3.0 LICENSE.

Copyright (C) 2021  Matt Belfast Brown
Copyright (C) 2021  MWAFU LIBRARY LOVE BOOK STORE

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


'''
import author_number as an
import pypinyin as pn

def get_pronouncation(alte_word):
    pron_ounc=pn.pinyin(alte_word,heteronym=True,style=pn.Style.FIRST_LETTER)
    return pron_ounc

def fetchcode(inpt_name):
    surn_name,last_name=an.fun_surn_disc(inpt_name)
    surn_pron=get_pronouncation(surn_name)
    last_pron=get_pronouncation(last_name)
    if len(surn_pron[0])==1:
        fist_char=surn_pron[0][0]
        if len(last_pron[0])==1:
            last_code=an.fun_take_code(surn_name,last_pron[0][0])
            return [fist_char,last_code]
        else:
            return [fist_char,last_pron]
    else:
        if len(last_pron[0])==1:
            return [surn_pron,last_pron[0][0]]
        else:
            return [surn_pron,last_pron]

