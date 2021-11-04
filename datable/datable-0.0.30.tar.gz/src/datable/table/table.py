import tkinter as tk
from .tksheet import Sheet
import platform
import os, re

class Datable:
    '''
[[SAMPLE]]
    |||This Class is for displaying data with a dynamic data table, which work like the data grid in sql developer.
[[INFO]]
    |||INFO: Header is not valid. You are expected to send out a header list with {0} column(s), but we received {1}. Therefore, header would be generated automatically.
    |||INFO: Datable descriptions:\n      Header    : {0};\n      Data Count: [{1}][{2}];
[[ERROR]]
    |||EROR: Cannot find key: {0};
    |||EROR: No Searching conditions were found;
    '''
    def _log(self, base, *format_):
        if len(format_) !=0:
            print(base.format(*format_)
        else:
            print(base)
            
    def _msg(self, key, item):
        dictionary = {'SAMPLE':1, 'INFO':2, 'EROR':3}
        mlst = self.__doc__.replace('[[SAMPLE]]', '[[__]]')\
                           .replace('[[INFO]]', '[[__]]')\
                           .replace('[[EROR]]', '[[__]]')\
                           .split('[[__]]')
        return mlst[dictionary[key]].split('|||')[item]

    def __init__(self, data=[], header=[]):
        if len(data[0]) == 0 and len(header)!=0:
            data = [['' * len(header)],]
        elif len(header) != len(data[0]) and len(data[0]) != 0:
            self._log(self._msg('INFO', 1), len(data[0]), len(header))
            header = [x + 1 for x in range(len(data[0]))]
        self.__data = data
        self.__header = header

    def __str__(self):
        return self._msg('INFO', 2).format(self.__header, len(self.__data), len(self.__data[0]))

    def __add__(self,other):
        newData = self.__data + other.__data
        return Datable(newData, self.__header)

    def __sub__(self,other):
        newData = list(filter(lambda x: x not in other.__data, self.__data))
        return Datable(newData, self.__header)

    def __and__(self,other):
        newData = list(filter(lambda x: x in other.__data, self.__data))
        return Datable(newData, self.__header)

    def __or__(self,other):
        x = self + other
        newData = []
        for each in x.__data:
            if each not in newData:
                newData.append(each)
        return Datable(newData, self.__header)

    def __getitem__(self, column_='', where=[(),]):
        def _T(key):
            if key in self.__header:
                dex = list(filter(None, ['{}'.format(i) if x == key else '' for i, x in enumerate(self.__header)]))
                T = zip(*self.__data)
                return T, int(dex[0])
            else:
                raise ValueError(self._msg('ERROR', 1).format(key))
        # Search by column name
        if column_!='':
            if type(column_) is str:
                T, dex = _T(column_)
                return zip(list(T)[dex])
            elif type(column_) is tuple:
                matrix = []
                for key in column_:
                    T, dex = _T(key)
                    matrix.append(list(T)[dex])
                return list(zip(*matrix))
        # Search by where clause
        elif len(where[0]) != 0:
            pass
        # No search conditions
        else:
            raise ValueError(self._msg('ERROR', 2))
    def __setitem__(self, column_, value):
        pass

    def __delitem__(self, column_):
        pass

    def show(self, bookmark=0):
        self.top = tk.Tk()
        if platform.system()=='Windows':
            from win32api import GetSystemMetrics
            Width = GetSystemMetrics(0)
            Height = GetSystemMetrics(1)
        elif platform.system()=='Darwin':
            results = list(filter(None,os.popen('system_profiler SPDisplaysDataType').read().replace(' ','').split('\n')))[13].replace(':','x').replace('R','x').split('x')
            Width, Height = int(results[2]), int(results[3])
        elif platform.system()=='Linux':
            resolution = os.system("xrandr  | grep \* | cut -d' ' -f4").split('x')
            Width = resolution[0]
            Height = resolution[1]


        sheet = Sheet(self.top, width=Width, height=Height, total_columns=len(self.__header))

        sheet.grid()
        sheet.headers(self.__header)
        sheet.set_sheet_data(self.__data)

        # table enable choices listed below:
        sheet.enable_bindings(("single_select", "row_select", "column_width_resize", "arrowkeys", "right_click_popup_menu", "rc_select", "rc_insert_row", "rc_delete_row", "copy", "cut", "paste", "delete", "undo", "edit_cell"))
        windowW = Width if (len(self.__header) * 120) + 23 > Width else len(self.__header) * 120 + 23
        windowH = Height if (len(self.__header) * 23) + 50 > Height else len(self.__header) * 23 + 50
        self.top.geometry("{}x{}".format(windowW, windowH))
        self.top.mainloop()