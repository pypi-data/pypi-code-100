#coding = utf-8
###
###by charles lan###
###邮箱:charles_kiko@163.com###
###

#blast数据取除自身之外的5个
import sys
from tqdm import trange

class filter_unit():
    def __init__(self, options):
        self.number = 10
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)


    def blasts(self):
        file = open(self.blast,'r').readlines()
        for i in trange(len(file)):
            line = file[i]
            lt=line.strip("\n").split()
            if lt[0] == lt[1]:
                continue
            if (str(lt[0]) not in blast):
                blast.append(str(lt[0]))
                number=int(self.number)
            else:
                if number != 0:
                    f.write(line)
                    number -= 1
                if number == 0:
                    continue

    def run(self):
        f = open(self.outfile,'w')
        blast=[]#储存blast信息的列表
        number=0
        self.blasts()
        f.close()
        sys.exit(0)