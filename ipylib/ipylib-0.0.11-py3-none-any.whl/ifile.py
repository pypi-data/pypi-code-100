# -*- coding: utf-8 -*-
import os
import re
import copy

from idebug import *



__all__ =[
    'get_filenames',
    'get_dirs',
    'get_filepaths',
    'open_file',
    'write_file',
]



def get_filenames(path):
    fnames = []
    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                fnames.append(entry.name)
    return sorted(fnames)


def get_dirs(path, alldepth=False):
    all_dirs = []
    for root, dirs, files in os.walk(top=path, topdown=True):
        if alldepth:
            for dir in dirs:
                all_dirs.append(dir)
        else:
            if root == path:
                all_dirs = dirs
                break
    return sorted(all_dirs)



def get_filepaths(path, alldepth=True, topdown=True):
    filepaths = []
    for root, dirs, files in os.walk(top=path, topdown=topdown):
        for file in files:
            if alldepth:
                filepaths.append(os.path.join(root, file))
            else:
                if root == path:
                    filepaths.append(os.path.join(root, file))
    filepaths = [e for e in filepaths if e not in ['.DS_Store']]
    return sorted(filepaths)



def open_file(filepath):
    dbg.printer(f"filepath : {filepath}")
    try:
        with open(file=filepath, mode='r') as f:
            text = f.read()
            f.close()
            return text
    except Exception as e:
        dbg.exception(locals(), f"{__name__}.open_file")


def _makedirs(filepath):
    try:
        os.makedirs(os.path.dirname(filepath))
    except Exception as e:
        pass



def write_file(filepath, text):
    dbg.printer(f"filepath : {filepath}")
    _makedirs(filepath)
    with open(file=filepath, mode='w') as f:
        f.write(text)
        f.close()

# ============================================================
"""파일/폴더명 중 일부 용어 변경."""
# ============================================================

rootdir = '/Users/sambong/Career/UPV/courses'

def convert_space_of_dir(rootdir, repl='-'):
    p_spc = re.compile('\s')
    for root, dirs, files in os.walk(top=rootdir, topdown=True):
        for dir in dirs:
            if p_spc.search(dir) is not None:
                print(f"{'-'*60} {dir}")
                print(os.path.join(root, dir))
                newdir = dir.replace(' ',repl)
                print(os.path.join(root, newdir))
                os.rename(os.path.join(root, dir), os.path.join(root, newdir))

def convert_space_of_file(rootdir, repl='-'):
    p_spc = re.compile('\s')
    for root, dirs, files in os.walk(top=rootdir, topdown=True):
        for file in files:
            m = p_spc.search(file)
            if m is not None:
                print(f"{'-'*60}\n{m}")
                print(os.path.join(root, file))
                newfile = file.replace(' ',repl)
                print(os.path.join(root, newfile))
                os.rename(os.path.join(root, file), os.path.join(root, newfile))

convert_space_of_file('/Users/sambong/pjts/iportfolio/home/static/home/images/responsive/thesis')

def convert_underbar_of_dir(rootdir, repl='__'):
    p_ubar = re.compile('[a-zA-Z0-9]_[a-zA-Z0-9]')
    p_excep = re.compile('^\.')
    for root, dirs, files in os.walk(top=rootdir, topdown=True):
        for dir in dirs:
            if p_excep.search(dir) is not None:
                pass
            else:
                if p_ubar.search(dir) is not None:
                    print(f"{'-'*60} {dir}")
                    print(os.path.join(root, dir))
                    newdir = copy.copy(dir)
                    for m in p_ubar.finditer(newdir):
                        newsdirli = list(newdir)
                        newsdirli.insert(m.start()+2, '_')
                        newdir = "".join(newsdirli)
                    #newdir, num = p_ubar.subn(repl=repl, string=dir)
                    print(os.path.join(root, newdir))
                    #os.rename(os.path.join(root, dir), os.path.join(root, newdir))


def convert_words_of_dir(rootdir, words_map):
    for root, dirs, files in os.walk(top=rootdir, topdown=True):
        for dir in dirs:
            for k,v in words_map.items():
                if re.search(k, dir) is not None:
                    print(f"{'-'*60} {dir}")
                    print(os.path.join(root, dir))
                    newdir, n = re.subn(pattern=k, repl=v, string=dir)
                    print(os.path.join(root, newdir))
                    os.rename(os.path.join(root, dir), os.path.join(root, newdir))
