import json
import os
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return True
class CopeJSON:
    def __init__(self, name):
        self.name = name
        if find(name+".json", os.getcwd()):
            pass
        else:
            with open(self.name + ".json", "w") as f:
                json.dump([], f, indent=4)
                f.close()

    def setColumn(self, column):
        self.column = column.split(",")
        self.columnlist = []

    def addColumn(self, column):
        column = column.split(",")
        for i in range(len(self.column)):
            for i2 in range(len(column)):
                if self.column[i] == column[i2]:
                    print("Name of column is duplicate")
                    return

        with open(self.name + ".json", "r") as f:
            temp = json.load(f)

        for i in range(len(column)):
            self.column.append(column[i])

        for i in range(len(temp)):
            for i2 in range(len(column)):
                temp[i][column[i2]] = "Null"

        with open(self.name + ".json", "w") as f:
            json.dump(temp, f, indent=4)

    def addData(self, data):
        data = data.split(",")
        Data = {}
        with open(self.name + ".json", "r") as f:
            temp = json.load(f)
        for i in range(len(self.column)):
            try:
                if len(self.columnlist) == 0:
                    Data[self.column[i]] = data[i]
                else:
                    for i2 in range(len(self.columnlist)):
                        if self.column[i] == self.columnlist[i2]:
                            Data[self.column[i]] = []
                            Data[self.column[i]].append(data[i])
                        else:
                            Data[self.column[i]] = data[i]
            except:
                if len(self.columnlist) == 0:
                    Data[self.column[i]] = "Null"
                else:
                    for i2 in range(len(self.columnlist)):
                        if self.column[i] == self.columnlist[i2]:
                            Data[self.column[i]] = []
                        else:
                            Data[self.column[i]] = "Null"

        temp.append(Data)
        with open(self.name + ".json", "w") as f:
            json.dump(temp, f, indent=4)

    def removeData(self, column, info):
        with open(self.name + ".json", "r") as f:
            temp = json.load(f)
        for i in range(len(temp)):
            for i2 in range(len(self.column)):
                if self.column[i2] == column:
                    if info == temp[i][self.column[i2]]:
                        temp.pop(i)

        with open(self.name + ".json", "w") as f:
            json.dump(temp, f, indent=4)

    def getData(self, select = "*", where = "", column = ""):
        if select == "*":
            if where == "":
                with open(self.name + ".json", "r") as f:
                    temp = json.load(f)
                return temp
            else:
                try:
                    where = where.split(",")
                    column = column.split(",")
                    result = []
                    with open(self.name + ".json", "r") as f:
                        temp = json.load(f)
                    for i in range(len(temp)):
                        data = {}
                        check = 0
                        for i2 in range(len(where)):
                            if temp[i][where[i2]] == column[i2]:
                                check = check + 1
                        if check == len(where):
                            for i2 in range(len(self.column)):
                                data[self.column[i2]] = temp[i][self.column[i2]]
                            result.append(data)
                    return result
                except:
                    print("Some Error")

        else:
            if where == "":
                try:
                    select = select.split(",")
                    result = []
                    with open(self.name + ".json", "r") as f:
                        temp = json.load(f)
                    for i in range(len(temp)):
                        data = {}
                        for i2 in range(len(select)):
                            data[select[i2]] = temp[i][select[i2]]
                        result.append(data)
                    return result
                except:
                    print("Some Error")
            else:
                try:
                    select = select.split(",")
                    where = where.split(",")
                    column = column.split(",")
                    result = []
                    with open(self.name + ".json", "r") as f:
                        temp = json.load(f)
                    for i in range(len(temp)):
                        data = {}
                        check = 0
                        for i2 in range(len(where)):
                            if temp[i][where[i2]] == column[i2]:
                                check = check + 1
                        if check == len(where):
                            for i2 in range(len(select)):
                                data[select[i2]] = temp[i][select[i2]]
                            result.append(data)
                    return result

                except:
                    print("Some Error")

    def editData(self, set, data, where, info):
        try:
            where = where.split(",")
            info = info.split(",")
            set = set.split(",")
            data = data.split(",")
            with open(self.name + ".json", "r") as f:
                temp = json.load(f)

            for i in range(len(temp)):
                check = 0
                for i2 in range(len(where)):
                    if temp[i][where[i2]] == info[i2]:
                        check = check + 1
                if check == len(where):
                    for i3 in range(len(set)):
                        temp[i][set[i3]] = data[i3]

            with open(self.name + ".json", "w") as f:
                json.dump(temp, f, indent=4)
        except:
            print("Some Error")

    def columnList(self, column):
        try:
            self.columnlist.append(column)
        except:
            print("some error")

    def addLists(self, column, where, value, data):
        try:
            with open(self.name + ".json", "r") as f:
                temp = json.load(f)
            for i in range(len(temp)):
                if temp[i][where] == value:
                    temp[i][column].append(data)
            with open(self.name + ".json", "w") as f:
                json.dump(temp, f, indent=4)
        except:
            print('some error')