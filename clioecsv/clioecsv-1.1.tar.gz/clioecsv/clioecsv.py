import os


def import_csv_as_list(filename, split_by=","):
    """ Import text or csv file with default seperator = ","

    parameters:
    file_name (str): The path to a text or csv file (string or raw string)
    split_by (str): The text file delimiter

    returns:
    list: The content of the text or csv file as list
    """
    read_lines = []
    with open(filename) as csv:
        for line in csv:
            read_lines.append(line.strip().split(split_by))
    return read_lines


def distinct_by_column(list, distinct_by_column=1):  # excel column start from 1
    """ Convert list into distinct record with default column 1 as key, ie. distinct_by_column(list, 1)

    parameters:
    list (list): The list of records ie: txt or csv file as a list
    distinct_by_column (int): column number for the distinct record with default column 1

    returns:
    dict_values: The distinct record return as dict_values (list)
    """
    dict = {}
    for line in list:
        dict[line[distinct_by_column-1]] = line
    return dict.values()


def distinct_by_columns(list, *distinct_by_columns):  # excel column start from 1
    """ Convert list into distinct record with multiple columns as key, ie. distinct_by_columns(list, 1, 2)

    parameters:
    list (list): The list of records ie: txt or csv file as a list
    *distinct_by_columns (int(s)): multiple columns as the distinct record's key

    returns:
    dict_values: The distinct record return as dict_values (list)
    """
    dict = {}
    for line in list:
        distinct_key = ""
        for column in distinct_by_columns:
            distinct_key += line[column-1]

        dict[distinct_key] = line
    return dict.values()


# combination of the above 2 functions, distinct_by_column(s) can be int or list
def distinct_list_bycolumns(list, distinct_by_columns):   # not tested
    """ Convert list into distinct record with default column 1 as key.
    ie.
    distinct_list_bycolumns(lines, 2)
    distinct_list_bycolumns(list, [1, 2])

    parameters:
    list (list): The list of records ie: txt or csv file as a list
    distinct_by_column(s) (int or list of integer): single or multiple columns as the distinct record's key

    returns:
    dict_values: The distinct record return as dict_values (list)
    """
    dict = {}
    print(type(distinct_by_columns))
    if type(distinct_by_columns) == type([1, 2]):
        for line in list:
            distinct_key = ""
            for column in distinct_by_columns:
                distinct_key += line[column-1]
            dict[distinct_key] = line
    else:
        for line in list:
            dict[line[distinct_by_columns-1]] = line
    return dict.values()


def sort_list(list, by_column, descending=False, header=True):
    """ Sort list by a particular column number.
    Note that you can import your csv or text file using function import_csv_as_list(filename, split_by=",").

    parameters:
    list (list): input data for data transformation
    by_column (int): column number where you want your list to be sorted
    descending (boolean): default is ascending order
    """
    list.sort(key=lambda item: item[by_column-1], reverse=descending)


def sorted_list(list, by_column, descending=False, header=True):
    """ Sort list by a particular column number.
    Note that you can import your csv or text file using function import_csv_as_list(filename, split_by=",").

    parameters:
    list (list): input data for data transformation
    by_column (int): column number where you want your list to be sorted
    descending (boolean): default is ascending order

    return:
    list: sorted list
    """
    header_line = []
    if header:
        header_line = list[:1]
        list = list[1:]
    newlist = sorted(
        list, key=lambda item: item[by_column-1], reverse=descending)
    return header_line+newlist


def remove_blank_top(list, by_column):
    """ remove the blank line on the top, choose column number where the first non blank row of that column will be the header.
    Note that you can import your csv or text file using function import_csv_as_list(filename, split_by=",").

    parameters:
    list (list): input data for data transformation
    by_column (int): column number where the first non blank row of that column will be the header
    """
    cur_row = 0
    while cur_row < len(list):
        if list[cur_row][by_column-1] == "":
            cur_row += 1
        else:
            break
    while (cur_row > 0):
        del list[cur_row - 1]
        cur_row -= 1
    return list


def remove_blank_bottom(list, by_column):
    """ Remove the bottom blank line of your text file, choose the column number where the first non blank row of that column will be the last row.
    Note that you can import your csv or text file using function import_csv_as_list(filename, split_by=",").

    parameters:
    list (list): input data for data transformation
    by_column (int): column number where you want your rows of data stop at.
    """
    last_row = len(list) - 1
    while (last_row >= 0):
        if list[last_row][by_column-1] == "":
            del list[last_row]
            last_row -= 1
        else:
            break
    return list


def export_to_csv(list, file_name, split_by=','):
    """ Export list to text file with comma delimiter or default delimiter = ",".

    parameters:
    list (list): data to be exported
    file_name (str): the path to a text file (string or raw string)
    split_by (str) the delimiter for the text or csv file

    returns:
    csv or text file: the output can be .txt or .csv format depends on how you name your file_name parameter.
    """
    with open(file_name, "w") as fin:
        for line in list:
            fin.write(split_by.join(line) + "\n")


def append_file(master_file_name, file_source, remove_header_line_number=0, remove_bottom_line_number=0):
    """ Function to combine a file with existing master_file_name. ie.: append_file("data/master.csv, "data/today_file.csv").

    parameters:
    master_file_name (str): the path and full name of master file name.
    file_source (str): the path and full name of the file to be added
    remove_header_line_number (int): how many header lines to skip
    remove_bottom_line_number (int): how many tail lines to skip
    """
    if os.path.exists(master_file_name):
        with open(master_file_name, "a") as wr:
            with open(file_source) as content:
                if content:
                    list_content = list(content)
                    last_line = len(list_content) - remove_bottom_line_number
                    wr.writelines(
                        list_content[remove_header_line_number:last_line])
    else:
        with open(master_file_name, "w") as wr:
            with open(file_source) as content:
                wr.writelines(list(content))


def merge_files(merge_file_name, list_of_file_sources, write_mode="a", remove_header_line_number=0, remove_bottom_line_number=0):
    """ Function to merge list of files into 1 file. ie: merge_files(merge_file_name, ["data/file1", "data/file2"], "a", 1, 0) # Remove Header

    parameters:
    merge_file_name (str): the path and full name of the merge file name.
    list_of_file_sources (list): list of files that need to be combined
    write_mode (str): "w" for write and "a" for append existing file (Note: case sensitive)
    remove_header_line_number (int): how many header lines to skip
    remove_bottom_line_number (int): how many tail lines to skip

    return a combine text or csv file with file name as per the merge_file_name
    """
    with open(merge_file_name, write_mode) as wr:
        for file in list_of_file_sources:
            with open(file) as content:
                if content:
                    list_content = list(content)
                    last_line = len(list_content) - remove_bottom_line_number
                    wr.writelines(
                        list_content[remove_header_line_number:last_line])
