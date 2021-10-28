#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def replace(theStr,sign0,sign1):
    """把str中的sign0替换成sign1"""
    #return reduce(lambda x,y:x+sign1+y,re.split(sign0,theStr))
    return reduce(lambda x,y:x+sign1+y,theStr.split(sign0))
#

def print_dict(d):
    """打印字典"""
    l = d.keys()
    l.sort()
    for key in l:
        print (key, ':', d[key])
    #
#

def replace_special(theStr,sign0,sign1):
    """把str中的sign0替换成sign1,当符号是单个特殊符号时"""
    thatStr = ''
    for i in range(len(theStr)):
        if theStr[i]==sign0:
            thatStr = thatStr+sign1
        else:
            thatStr = thatStr+theStr[i]
        #
    #
    return thatStr
#

def replace_special_u(theStr,sign0,sign1):
    """把str中的sign0替换成sign1,当符号是单个特殊符号时,全都是unicode"""
    thatStr = u''
    for i in range(len(theStr)):
        if theStr[i]==sign0:
            thatStr = thatStr+sign1
        else:
            thatStr = thatStr+theStr[i]
        #
    #
    return thatStr
#

#把str2插入到str1的任意位置：unite_strs('01234','xx',3) -> return '012xx34' (str1[3]='3')
def unite_strs(str1,str2,n):
    return str1[:n]+ str2[:] + str1[n:]
#

#('"abc"','def') -> '"abcdef"'
#('abc','def')以及其他 -> 'abcdef'
def full_path(folderStr,fileNameStr):
    if folderStr[-1:] == '"' and folderStr[:1] == '"':
        return unite_strs(folderStr,fileNameStr,-1)#代替return folderStr[:-1]+fileNameStr+'"'
    else:
        return folderStr + fileNameStr
#

#(['aaaaa',offset,'bbbbb',],m,n) -> ['aaaaa<m+offset>bbbbb',...'aaaaa<n+offset>bbbbb']
def loop_increaser(selectorForm,m,n):
    f = lambda i:selectorForm[0]+str(i)+selectorForm[2]
    return map(f,range(m+selectorForm[1],n+1+selectorForm[1]))
#

def is_str_included(string,f):
    """判断f中是否含有字符串string"""
    n_of_string = len(string)
    times = len(f)-n_of_string+1
    while times >= 1:
        part = f[times-1:times-1+n_of_string]
        if part == string:
            #print f
            return True
        else:
            times = times - 1
        #
    #
    return False
#

def is_include_str(f,string):
    """判断f中是否含有字符串string"""
    n_of_string = len(string)
    times = len(f)-n_of_string+1
    while times >= 1:
        part = f[times-1:times-1+n_of_string]
        if part == string:
            #print f
            return True
        else:
            times = times - 1
        #
    #
    return False
#

#conj_str_list的作用是把一个形如['Hello','world']的list变成一个字符串：‘Hello world‘
#(['Hello','world','fdsf']) -> ‘Hello world fdsf‘
def conj_str_list(l):
    conj = l[0]
    position = 1
    while position < len(l):
        conj = conj + ' '+ l[position]
        position = position + 1
    return conj
#

# def read_str_until(theStr,sign):
#     out = ''
#     for char in theStr:
#         if char!=sign:
#             out = out + char
#         else:
#             break
#         #
#     #
#     return out
# #
#('hello,word',',w') -> 'hello'
def read_str_until(theStr,sign):
    return re.split(sign,theStr)[0]
#

#('"') -> ''
#('"..."') -> '...'
def remove_double_quotes(theStr):
    if theStr[:1]=='"' and theStr[-1:]=='"':
        theStr = theStr[1:-1]
    #
    return theStr
#


def print_strList_red(theStrList, mod=0,gapSign='\n', maxLinesPerItem=5):
    outPut = ''
    for i in range(len(theStrList)):
        if mod == 0:
            outPut += '\033[1;31m%d:\033[0m  ' % (i)
        splited = theStrList[i].split('\n')
        oneItem = ''
        for j in range(min(len(splited), maxLinesPerItem)):
            oneItem += '%s%s' % (splited[j],'\n')
        if oneItem != '':
            outPut += oneItem[:-1]
        if mod != 0:
            outPut += '   \033[1;31m%d:\033[0m' % (i)
        outPut += gapSign
    #
    outPut = outPut[:-len(gapSign)]
    print (outPut)
#


def print_strList(theStrList,mod=0,gapSign='\n'):
    outPut = ''
    if mod ==0:
        for i in range(len(theStrList)):
            outPut += '%d:  %s%s' % (i,theStrList[i],gapSign)
        #
    else:
        for i in range(len(theStrList)):
            outPut += '%s   :%d%s' % (theStrList[i],i,gapSign)
        #
    #
    outPut = outPut[:-len(gapSign)]
    print (outPut)
#


def print_strMap(theStrMap,mod=0,gapSign='\n'):
    outPut = ''
    if mod ==0:
        index = 0;
        for key in theStrMap:
            val = theStrMap[key]
            outPut += '%d   %s: %s%s' % (index,key,val,gapSign)
            index +=1
        #
    else:
        index = 0;
        for key in theStrMap:
            val = theStrMap[key]
            outPut += '%s: %s   :%d%s' % (key,val,index,gapSign)
        #
        index +=1
    #
    outPut = outPut[:-len(gapSign)]
    print (outPut)
#


def return_print_strList_simple(theStrList,gapSign='\n'):
    outPut = ''
    for i in range(len(theStrList)):
        outPut += theStrList[i] + gapSign
    #
    outPut = outPut[:-len(gapSign)]
    return outPut
#
def print_strList_simple(theStrList,gapSign='\n'):
    outPut = return_print_strList_simple(theStrList,gapSign)
    print (outPut)
#
