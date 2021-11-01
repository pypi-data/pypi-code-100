
# = file to list converter

# ¤ takes file as string input, a variable for the file (it can be whatever as long as it is changeable) and an empty list as input
def file_lister(file):
    file_variable = open(file, "r")  # ¤ opens file in variable
    file_list = file_variable.readlines()  # ¤ writes file content to list
    for i in range(len(file_list)):  # ¤ strips the content of the list
        file_list[i] = file_list[i].strip()
    file_variable.close()  # ¤ closes file
    return file_list  # ¤ returns the list

