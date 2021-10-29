##==========~~~~~~~~~~==========~~REMARK~~==========~~~~~~~~~~==========##
## Code:    Python Plot Style
## Author:  Wende Li
## Email:   wende.li@outlook.com
## Version:
## >>       1.0: plot setup completed based on python matplotlib
## General:
## >>       This plot style is suitable for pictures in paper publication
## >>       Install matplotlib: python -m pip install -U matplotlib
## >>       Reference: matplotlib.org
## >>       Reference: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
##==========~~~~~~~~~~==========~~~~~~~~~~==========~~~~~~~~~~==========##


##==========~~~~~~~~~~==========~~IMPORT~~==========~~~~~~~~~~==========##
## DEPENDENT MODULES
import os
import sys
import glob
import numpy as np
import pandas as pd
import matplotlib as mpl
##==========~~~~~~~~~~==========~~~~~~~~~~==========~~~~~~~~~~==========##


##==========~~~~~~~~~~==========~FUNCTION~==========~~~~~~~~~~==========##
def plot_setup(font_size='8'):
    ''' define font size of generated pictures
    '''
    if not isinstance(font_size,str):
        print(_ERROR_+' font_size '+f'{font_size}')
        sys.exit(_STR_ERROR_)

    font_name = 'sans-serif'

    mpl.rcParams['font.family']         =   font_name   # default text font name
    mpl.rcParams['font.size']           =   font_size   # default text font size
    mpl.rcParams['axes.titlesize']      =   font_size   # fontsize of the title
    mpl.rcParams['axes.labelsize']      =   font_size   # fontsize of the labels
    mpl.rcParams['xtick.labelsize']     =   font_size   # fontsize of the x ticks
    mpl.rcParams['ytick.labelsize']     =   font_size   # fontsize of the y ticks

    mpl.rcParams['legend.fontsize']     =   font_size   # fontsize of the legend
    mpl.rcParams['legend.frameon']      =   False       # frame of the legend
    mpl.rcParams["legend.labelspacing"] =   0.2         # space of legend entries, font-size units

    mpl.rcParams['lines.linewidth']     =   1.2
    mpl.rcParams['lines.markersize']    =   4
    mpl.rcParams['lines.linestyle']     =   '-'

    mpl.rcParams['figure.figsize']      =   (4, 3)      # figure size (width, height) in inches
    mpl.rcParams['figure.dpi']          =   100         # dots per inch

    mpl.rcParams['axes.autolimit_mode'] = 'data'        # offset of axes
    mpl.rcParams['axes.xmargin']        = 0.
    mpl.rcParams['axes.ymargin']        = 0.

def plot_reset():
    ''' reset the plot configuration
    '''
    plot_setup(font_size='8')

def read_data(file_name,use_cols=None,d_type='a',skip_rows=0,skip_blank=True,clean_data=False):
    ''' read data from a file
        file_name: file path or file name string (e.g. './data/file.txt')
        d_type: data type for data or columns, e.g. {‘a’: np.float64, ‘b’: np.int32, ‘c’: ‘Int64’}
    '''
    if not isinstance(file_name,str):
        print(_ERROR_+' file_name '+f'{file_name}')
        sys.exit(_STR_ERROR_)
    if not isinstance(skip_rows,int):
        print(_ERROR_+' skip_rows '+f'{skip_rows}')
        sys.exit(_INT_ERROR_)
    if use_cols:
        if not isinstance(use_cols,list):
            print(_ERROR_+' use_cols '+f'{use_cols}')
            sys.exit(_LIST_ERROR_)
        if not all(isinstance(i,int) for i in use_cols):
            print(_ERROR_+' element of use_cols '+f'{use_cols}')
            sys.exit(_INT_ERROR_)
    if not isinstance(d_type,str):
        print(_ERROR_+' d_type '+f'{d_type}')
        sys.exit(_STR_ERROR_)
    if not isinstance(skip_blank,bool):
        print(_ERROR_+' skip_blank '+f'{skip_blank}')
        sys.exit(_BOOL_ERROR_)
    if not isinstance(clean_data,bool):
        print(_ERROR_+' clean_data '+f'{clean_data}')
        sys.exit(_BOOL_ERROR_)

    data_read = file_name+'.txt'
    if use_cols:
        data_temp = pd.read_csv(file_name,
                                usecols=use_cols,
                                dtype=d_type,
                                skiprows=skip_rows,
                                skip_blank_lines=skip_blank,
                                delim_whitespace=True)
    else:
        data_temp = pd.read_csv(file_name,
                                dtype=d_type,
                                skiprows=skip_rows,
                                skip_blank_lines=skip_blank,
                                delim_whitespace=True)
    data_temp.to_csv(data_read,index=False)
    # clean data before use
    if clean_data:
        clean_data_by_rules(data_read)
    data = np.loadtxt(data_read,delimiter=',')

    # delete temporary data read file
    if os.path.exists(data_read):
        try:
            os.remove(data_read)
        except PermissionError:
            print('No permission to delete the temporary file <'+data_read+'>')
        except:
            print('Undefined error occurred to delete the temporary file <'+data_read+'>')

    return data

def clean_data_by_rules(file_name):
    ''' replace unnecessary strings in data file with nan for matplotlib
        input file should contain text data
    '''
    with open(file_name, 'r') as file :
        file_data = file.read()

    # add more rules if needed
    file_data = file_data.replace('#,z','nan,nan') # replace '#,z'
    file_data = file_data.replace(',\n','nan,nan\n') # replace ',\n'

    with open(file_name, 'w') as file:
        file.write(file_data)

def find_file(dir_path,file_name,sort=True):
    """ find the file from provided directory
        (1) dir_path should be a string
        (2) file_name could be a string or a list
    """
    if not isinstance(dir_path,str):
        print(_ERROR_+' dir_path '+f'{dir_path}')
        sys.exit(_STR_ERROR_)

    # a directory can be a string or a list containing strings
    if not isinstance(file_name,(str,list)):
        print(_ERROR_+' file_name '+f'{dir_path}')
        sys.exit(_STR_LIST_ERROR_)

    # change a string to a list
    if not isinstance(file_name,list):
        file_name = [file_name]

    # avoid non-string element in a list
    if not all(isinstance(i,str) for i in file_name):
        print(_ERROR_+' file_name '+f'{dir_path}')
        sys.exit(_STR_LIST_ERROR_)

    if not isinstance(sort,bool):
        print(_ERROR_+' sort '+f'{sort}')
        sys.exit(_BOOL_ERROR_)

    path_name_list = []
    for i in range(len(file_name)):
        path_name_list.append(os.path.join(dir_path,file_name[i]))

    file_list = []
    for i in range(len(path_name_list)):
        file_list += [os.path.basename(x) for x in glob.glob(path_name_list[i])]

    if sort:
        file_list.sort()

    if len(file_list) != 0:
        return file_list
    else:
        sys.exit(_ERROR_+' no file found in <'+dir_path+'>')
##==========~~~~~~~~~~==========~~~~~~~~~~==========~~~~~~~~~~==========##


##==========~~~~~~~~~~==========~~~ERROR~~==========~~~~~~~~~~==========##
## DEFINE OUTPUT ERRORS
_ERROR_                 = 'Error:'

# ERROR SOLUTION
_INT_ERROR_             = 'Input Should be an Integer.'
_INT_SIGN_ERROR_        = 'Input Integer Should Non-Negative.'
_STR_ERROR_             = 'Input Should be a String.'
_INT_STR_ERROR_         = 'Input Should be an Integer or a String.'
_FLOAT_ERROR_           = 'Input Should be an Float Number.'
_INT_FLOAT_ERROR_       = 'Input Should be an Integer or a Float Number.'
_LIST_ERROR_            = 'Input Should be a List.'
_STR_LIST_ERROR_        = 'Input Should be a String or a List of Strings.'
_DICT_ERROR_            = 'Input Should be a Dictionary.'
_DICT_KEY_ERROR_        = 'Config Data Missing.'
_BOOL_ERROR_            = 'Input Should be a Boolean.'
##==========~~~~~~~~~~==========~~~~~~~~~~==========~~~~~~~~~~==========##