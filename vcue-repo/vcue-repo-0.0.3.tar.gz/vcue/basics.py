import sys
sys.path.append('../')

import bz2, os, itertools
import numpy as np
import pandas as pd
import _pickle as pickle
from itertools import groupby
import random, string 
import importlib

def rename(data, oldnames, newname): 
    '''Rename variable names in a dataset, returns a dataframe with new names ~ 
    df.columns = ['var1','var2'....'var30']
    df = rename(df, ['var1','var25'], ['name','id'])
    __________
    parameters
    - data : pd.DataFrame
    - oldnames : str or list of str. Variable names you want to rename 
    - newname : str or list of str. New variable names, must be of same length as oldnames 
    '''
    if type(oldnames) == str:
        oldnames = [oldnames]
        newname = [newname]
    i = 0 
    for name in oldnames:
        oldvar = [c for c in data.columns if name in c]
        if len(oldvar) == 0: 
            raise ValueError("Sorry, couldn't find "+str(name)+" column in the dataset")
        if len(oldvar) > 1: 
            print("Found multiple columns that matched " + str(name) + " :")
            for c in oldvar:
                print(str(oldvar.index(c)) + ": " + str(c))
            ind = input('please enter the index of the column you would like to rename: ')
            oldvar = oldvar[int(ind)]
        if len(oldvar) == 1:
            oldvar = oldvar[0]
        data = data.rename(columns = {oldvar : newname[i]})
        i += 1 
    return data   

def import_full_excel(xl_file):
    '''Returns a dictionary with the sheet names as keys and the data as values
    - xl_file : string. filepath to excel file 
    '''
    xls = pd.ExcelFile(xl_file)

    db = {} 
    for sheet in xls.sheet_names: 
        db[sheet] = pd.read_excel(xls, sheet)    # read in the excel sheets 
        db[sheet] = db[sheet].fillna(0)          # fill in the missing values with 0's 
        for c in db[sheet].columns:              # make numeric fields integers
            try: 
                db[sheet][c] = db[sheet][c].astype(int)
            except: 
                pass
        
    print("Sheet names are: "+", ".join(list(db.keys())))

    return db

def meatloaf(left, right, left_on, right_on, leftovers='left_only'):
    '''Merge two datasets and return the merged and residuals'''
    mrg = pd.merge(left, right, left_on=left_on, right_on=right_on, how='outer', indicator=True) # merge the two datasets 
    # print(mrg['_merge'].value_counts())                                          
    residuals = mrg[mrg['_merge']==leftovers][left.columns]                      # get the data that didn't merge 
    mrg = mrg[mrg['_merge']=='both']                                             # keep the data that did merge 
    return mrg, residuals 

def getFilepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

def absoluteFilePaths(directory):
    '''Get the absolute file path for every file in the given directory'''

    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))

def full_value_count(data, col):
    '''Return the value count and percentages'''
    table = pd.merge(
        pd.DataFrame(data[col].value_counts().sort_index()),
        pd.DataFrame(data[col].value_counts().sort_index()/data[col].value_counts().sum()), 
        right_index=True, left_index=True, how='inner')
    table.columns = [col+'_#', col+'_%']
    return table 


def import_package_string(package_string):
    '''Submit a string argument to be imported as a package (i.e. day_trader.models.LU01_A3). No need to include the .py'''
    return importlib.import_module(package_string)

def genrs(length=10):
    '''Generate random string function'''
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def chunks(l,n):
    '''Break list l up into chunks of size n'''    
    for i in range(0, len(l), n):
        yield l[i:i+n]  

def sizeFirstBin(data, col, minimum_bin_size, vals=None):
    '''Bin the data based on the vals, iterates through each val assigning the corresponding rows to a bin while that bin size has not reached the minimum_bin_size
    __________
    parameters
    - data : pd.DataFrame
    - col : the columns to bin based on 
    - minimum_bin_size : int. Each bin must have at least this size
    - vals : list. Will only bin the values in this list. The default is all the unique values of "col" 
     '''
    if vals is None: 
        values = sorted(data[col].unique())
    else: 
        values = vals

    bins = {}
    bin_number = 1 
    bin_total = 0 
    vc = dict(data[col].value_counts())
    for val in values:

        if bin_total<minimum_bin_size: 
            if bin_number not in bins:             
                bins[bin_number] = [] 
                bins[bin_number].append(val)
                bin_total += vc[val]
            else: 
                bins[bin_number].append(val)            
                bin_total += vc[val]
        
        else: 
            bin_number+=1
            bins[bin_number] = [] 
            bins[bin_number].append(val)
            bin_total = vc[val]
        
    return bins

def nondups(items : list):
    '''Return True if list has no duplicate items'''

    print('List length:',len(items))
    print('Unique items:',len(set(items)))
    
    return len(items) == len(set(items))
    
def order(frame, var):
    '''Brings the var to the front of the dataframe. e.g. df = order(df, ['col4','col12'])
    
    - frame : pandas dataframe
    - var : str or list of str. Variables you want to bring to the front. 
    '''
    if type(var) == str:
        var = [var]          
    varlist =[w for w in frame.columns if w not in var]
    frame = frame[var+varlist]
    return frame   
    
# Article on pickling and compressed pickling functions 
# https://betterprogramming.pub/load-fast-load-big-with-compressed-pickles-5f311584507e

def full_pickle(title, data):
    '''pickles the submited data and titles it'''
    pikd = open(title + '.pickle', 'wb')
    pickle.dump(data, pikd)
    pikd.close()   
    
def loosen(file):
    '''loads and returns a pickled objects'''
    pikd = open(file, 'rb')
    data = pickle.load(pikd)
    pikd.close()
    return data   

def compressed_pickle(title, data):
    '''
    Pickle a file and then compress it into a file with extension .pbz2
    __________
    parameters
    - title : title of the file you want to save (will be saved with .pbz2 extension automatically)
    - data : object you want to save 
    '''
    with bz2.BZ2File(title + '.pbz2', 'w') as f: 
        pickle.dump(data, f)

def decompress_pickle(filename):
    '''filename - file name including .pbz2 extension'''
    data = bz2.BZ2File(filename, 'rb')
    data = pickle.load(data)
    return data

def find(name, path):
    # Find the file name in any of the directories or sub-directories in the path 
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

# Time Stuff
def cuttomin(x):
    '''Cut a time stamp at the minutes (exclude seconds or more precise)'''
    return datetime.strftime(x, '%m-%d %H:%M')
    
def cuttohrs(x):
    '''Cut a time stamp at the hours (exclude minutes or more precise)'''
    return datetime.strftime(x, '%m-%d %H')

def cuttodays(x):
    '''Cut a time stamp at the date (exclude hour or more precise)'''
    return datetime.strftime(x, '%y-%m-%d')

def datetime_range(start, end, delta):
    '''Returns the times between start and end in steps of delta'''
    current = start
    while current < end:
        yield current
        current += delta

def prev_weekday(adate):
    '''Returns the date of the last weekday before the given date'''
    adate -= timedelta(days=1)
    while adate.weekday() > 4: # Mon-Fri are 0-4
        adate -= timedelta(days=1)
    return adate
