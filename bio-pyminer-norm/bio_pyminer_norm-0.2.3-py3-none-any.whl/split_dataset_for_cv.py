#!/usr/bin/env python3
##import dependency libraries
import sys,time,glob,os,pickle,fileinput,argparse,random
from subprocess import Popen, PIPE
from operator import itemgetter
import gc, fileinput
import numpy as np
import hashlib
try:
    from pyminer_norm.common_functions import process_dir
except:
    from common_functions import process_dir
#import pandas as pd
##############################################################
## basic function library
def read_file(tempFile,linesOraw='lines',quiet=False):
    if not quiet:
        print('reading',tempFile)
    f=open(tempFile,'r')
    if linesOraw=='lines':
        lines=f.readlines()
        for i in range(0,len(lines)):
            lines[i]=lines[i].strip('\n')
    elif linesOraw=='raw':
        lines=f.read()
    f.close()
    return(lines)

def make_file(contents,path):
    f=open(path,'w')
    if isinstance(contents,list):
        f.writelines(contents)
    elif isinstance(contents,str):
        f.write(contents)
    f.close()

    
def flatten_2D_table(table,delim):
    #print(type(table))
    if str(type(table))=="<class 'numpy.ndarray'>":
        out=[]
        for i in range(0,len(table)):
            out.append([])
            for j in range(0,len(table[i])):
                try:
                    str(table[i][j])
                except:
                    print(table[i][j])
                else:
                    out[i].append(str(table[i][j]))
            out[i]=delim.join(out[i])+'\n'
        return(out)
    else:
        for i in range(0,len(table)):
            for j in range(0,len(table[i])):
                try:
                    str(table[i][j])
                except:
                    print(table[i][j])
                else:
                    table[i][j]=str(table[i][j])
            table[i]=delim.join(table[i])+'\n'
    #print(table[0])
        return(table)


def strip_split(line, delim = '\t'):
    return(line.strip('\n').split(delim))

def make_table(lines,delim):
    for i in range(0,len(lines)):
        lines[i]=lines[i].strip()
        lines[i]=lines[i].split(delim)
        for j in range(0,len(lines[i])):
            try:
                float(lines[i][j])
            except:
                lines[i][j]=lines[i][j].replace('"','')
            else:
                lines[i][j]=float(lines[i][j])
    return(lines)


def get_file_path(in_path):
    in_path = in_path.split('/')
    in_path = in_path[:-1]
    in_path = '/'.join(in_path)
    return(in_path+'/')


def read_table(file, sep='\t'):
    return(make_table(read_file(file,'lines'),sep))
    
def write_table(table, out_file, sep = '\t'):
    make_file(flatten_2D_table(table,sep), out_file)
    

def import_dict(f):
    f=open(f,'rb')
    d=pickle.load(f)
    f.close()
    return(d)

def save_dict(d,path):
    f=open(path,'wb')
    pickle.dump(d,f)
    f.close()

def cmd(in_message, com=True, get_out = True):
    print('\n',in_message)
    time.sleep(.25)
    return
    if com:
        if get_out:
            out = Popen(in_message,shell=True,stdout=PIPE).communicate()
        else:
            Popen(in_message,shell=True).communicate()

    else:
        Popen(in_message,shell=True)
    if com and get_out:
        return(out)
#######################################################################################




###############################################################
###############################################################

parser = argparse.ArgumentParser()


## global arguments
parser.add_argument(
    '-in_file','-i','-infile',
    type=str)

parser.add_argument(
    '-out_dir','-o',
    type=str)

parser.add_argument(
    '-name','-n',
    type=str,
    help="what is this dataset named? We'll use this for the 'leader string' to prepend to the cross-validation iters")

parser.add_argument(
    '-iters','-it','-iter',
    type=int)

parser.add_argument(
    '-fold','-fold_cv',
    type=int)

parser.add_argument(
    '-seed','-random_seed','-rand',
    default = 1234567890,
    type=int)


args = parser.parse_args()


###############################################################
###############################################################
print('setting seeds to',args.seed)
random.seed(args.seed)
np.random.seed(args.seed)

###############################################################
###############################################################

def get_fold_indices(n_fold):
    """
    Shuffle the indices, then digitize the indices creating a sliding window for n_folds.
    At the end we'll sort the indices.
    """
    global in_table
    n_cols = np.shape(in_table)[1]

    cols = np.arange(1,n_cols)
    np.random.shuffle(cols)
    print(cols)
    hold_out = int((n_cols-1)/n_fold)
    print(hold_out,'samples held out per fold')

    ## make the indices for cutoffs that will be held out
    indices = [0]
    for f in range(n_fold):
        indices.append(indices[-1]+hold_out)
    
    hold_out_indices = []
    for n in range(1,len(indices)):
        hold_out_indices.append([indices[n-1],indices[n]])
        #print(hold_out_indices[-1])

    keep_indices = []
    for n in hold_out_indices:
        first = cols[:n[0]].tolist()
        second = cols[n[1]:].tolist()
        temp_keep = first+second
        temp_keep = sorted(temp_keep)
        keep_indices.append(temp_keep)
        #print(keep_indices[-1])
        

    return(keep_indices)




###############################################################
## I wrote this script a long time ago & would definitely not 
## have done it like this again... Not sure why I thought a
## script calling itself instaed of a loop was a good idea at the time...
###############################################################

if args.iters == None:
    in_table = np.array(read_table(args.in_file),dtype=str)
    fold_indices = get_fold_indices(args.fold)
    for idxs in range(0,len(fold_indices)):
        temp_idxs = fold_indices[idxs]
        ## add the leader column
        temp_idxs = [0]+temp_idxs
        ## subset the array
        print(in_table[:,temp_idxs])
        out_dir = process_dir(args.out_dir)
        write_table(in_table[:,temp_idxs],os.path.join(out_dir,args.name+"_"+str(idxs)+'.tsv'))

else:
    ## figure out where this script is
    for it in args.iters:
        next_dir = args.out_dir+' iter_'+str(it)+'/'
        cmd('mkdir '+next_dir)
        next_rand = str(np.random.randint(10000,10000000))
        cmd("python3 "+sys.argv[0]+" -i "+args.infile+" -o "+next_dir+' -seed '+next_rand+' -fold '+str(args.fold)+' -name '+str(args.name))











