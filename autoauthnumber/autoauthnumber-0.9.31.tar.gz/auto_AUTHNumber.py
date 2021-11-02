'''This is a library about automatic number-taking of "General Chinese Author Number Table". 
   At present, there is only one way to take the number, that is, directly looking up the table.
   In the future, we will adapt to a variety of author numbering methods, please wait.
   
   You can use the distributecode() method or fetchcode() method to find the author number.'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import author_number as an
import pypinyin as pn
def fetchcode(name):
    surn_name,part=an.fun_surn_disc(name)
    if type(part)==dict:
        last_name=name.replace(surn_name,"")[0]
        pron_unci=pn.pinyin(last_name,heteronym=True,style=pn.Style.FIRST_LETTER)
        if len(pron_unci[0])==1:
            frst_letr=pron_unci[0][0].upper()
            name_code=part.get(frst_letr,frst_letr)
            auth_letr=pron_unci=pn.pinyin(surn_name,heteronym=True,style=pn.Style.FIRST_LETTER)[0][0].upper()
        auth_code=auth_letr+name_code
    else:
        auth_letr=pron_unci=pn.pinyin(surn_name,heteronym=True,style=pn.Style.FIRST_LETTER)[0][0].upper()
        name_code=part
        auth_code=auth_letr+name_code
    
    return auth_code
        
