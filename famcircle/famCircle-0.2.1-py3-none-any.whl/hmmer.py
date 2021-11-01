###hmmer 用隐马尔可夫模型来对pep中的序列进行筛选保留value小于1*10-20，得到一个基因家族初等的列表，然后根据列表提取出序列，\
###再用clustalw就行序列比对,再用生成的aln文件再构建隐马尔可夫模型，用新的隐马尔可夫模型再进行筛选。再提取。
# python
# -*- encoding: utf-8 -*-
'''
@File        :hmmer.py
@Time        :2021/09/28 11:23:06
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :扫描hmm
'''



import Bio
from glob import glob
from io import StringIO
from Bio.Align.Applications import MafftCommandline, ClustalwCommandline
from Bio import Seq
from Bio import SeqIO
from Bio import AlignIO
from Bio.SeqRecord import SeqRecord
import subprocess
from subprocess import Popen

import glob # 都是标准库的东西

import re
import os
from math import *
import csv
import pandas as pd
from matplotlib.patches import *
from pylab import *
from famCircle.bez import *
#system 阻塞
import platform

class hmmer():
    def __init__(self, options):
        self.cds = None
        base_conf = config()
        for k, v in base_conf:
            setattr(self, str(k), v)
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def readlist(self,filename,value):
        name = []
        f = open(filename, 'r', encoding='utf-8')
        for row in f:
            if row != '\n' and row[0] != '#':
                row = row.strip('\n').split()
                if eval(row[6]) < float(value):
                    if ('>' + str(row[0]) not in name):
                        name.append('>' + str(row[0]))
        if len(name) == 0:
            print("Warning: Screening is too strict!")
        return name

    def readpep(self):
        peplist = {}
        f =open(self.pep, 'r', encoding='utf-8')
        s = ''
        name = ''
        for row in f:
            if row[0] == '>':
                if s != '' and name != '':
                    peplist[name] = s
                    s = ''
                    name = ''
                name = row.strip('\n')
            elif row == '\n':
                pass
            else:
                s = s + row
        if s != '' and name != '':
            peplist[name] = s
        del name, s
        return peplist

    def readcds(self):
        cdslist = {}
        f =open(self.cds, 'r', encoding='utf-8')
        s = ''
        name = ''
        for row in f:
            if row[0] == '>':
                if s != '' and name != '':
                    cdslist[name] = s
                    s = ''
                    name = ''
                name = row.strip('\n')
            elif row == '\n':
                pass
            else:
                s = s + row
        if s != '' and name != '':
            cdslist[name] = s
        del name, s
        return cdslist

    def writepep(self,pash0,name,seq,file):
        f = open(pash0 + file, 'a+', encoding='utf-8')
        f.write(name + '\n')
        f.write(seq)
        f.close()

    def format_clustal(self,name0):
        stockholm = name0 + '.sto'
        with open(name0+'.aln', 'r') as fhandle: # 这个是读fasta文件用的，把所有fasta文件都保存到列表里
            fastas = ['>' + tmp.replace('\n', '\r', 1).replace('\n', '').replace('\r', '\n') for tmp in tuple(filter(None, (fhandle.read().split('>'))))]
        for i in range(len(fastas)):
            fastas[i] = fastas[i].split('\n')
            fastas[i][0] = '>'+fastas[i][0].split(';')[1]
            tmp = []
            for j in range(len(fastas[i][1]) // 80 + 1):
                tmp.append(fastas[i][1][80 * j : 80 * j + 80])
            fastas[i][1] = tmp
        with open(stockholm, 'w') as out: # 这里在写sto文件
            out.write('# STOCKHOLM 1.0\n\n')
            for j in range(len(fastas[0][1]) - 1):
                for i in range(len(fastas)):
                    out.write('% -s %s\n' % (fastas[i][0], fastas[i][1][j]))
                out.write('\n')
            for i in range(len(fastas)):
                out.write('% -s %s\n' % (fastas[i][0], fastas[i][1][-1]))
            out.write('//')
    def format_muscle(self,name0):
        stockholm = name0 + '.sto'
        with open(name0+'.aln', 'r') as fhandle: # 这个是读fasta文件用的，把所有fasta文件都保存到列表里
            fastas = ['>' + tmp.replace('\n', '\r', 1).replace('\n', '').replace('\r', '\n') for tmp in tuple(filter(None, (fhandle.read().split('>'))))]
        for i in range(len(fastas)):
            fastas[i] = fastas[i].split('\n')
            fastas[i][0] = fastas[i][0]
            tmp = []
            for j in range(len(fastas[i][1]) // 80 + 1):
                tmp.append(fastas[i][1][80 * j : 80 * j + 80])
            fastas[i][1] = tmp
        with open(stockholm, 'w') as out: # 这里在写sto文件
            out.write('# STOCKHOLM 1.0\n\n')
            for j in range(len(fastas[0][1]) - 1):
                for i in range(len(fastas)):
                    out.write('% -s %s\n' % (fastas[i][0], fastas[i][1][j]))
                out.write('\n')
            for i in range(len(fastas)):
                out.write('% -s %s\n' % (fastas[i][0], fastas[i][1][-1]))
            out.write('//')


    def runhmm(self, hmmmold, path):
        names = hmmmold[:-4]
        hmmer = self.hmmer_path
        hmmsearch = hmmer + 'hmmsearch'
        hmmbuild = hmmer + 'hmmbuild'
        m1 = hmmsearch + ' --domtblout one.out -E ' + self.e_value1 + ' ' + hmmmold + ' ' + self.pep
        if os.path.exists('one.out'):
            os.remove ('one.out')
        d = os.system(m1)# 第一次搜索
        list1 = self.readlist('one.out',self.e_value1)# 第一次筛选
        os.remove ('one.out')
        if len(list1) == 0:
            print('STEP 1 :No data fit the model')
            return 0
        peplist = self.readpep()
        if os.path.exists('one.pep'):
            os.remove ('one.pep')
        for i in list1:# 第一次生成筛选之后的pep
            if i in peplist.keys():
                seq = peplist[i]
                pash0 = './'
                self.writepep(pash0,i,seq,'one.pep')
            else:
                pass
        in_file = 'one.pep'
        if platform.system() == 'Windows':
            name0 = str(names.split('\\')[-1])
        else:
            name0 = str(names.split('/')[-1])
        out_file ='./out_aln/' + name0 + '.aln'
        if (self.comparison == "clustal"):
            self.clustalw_path = self.clustalw_path
            print(self.clustalw_path,in_file,out_file)
            Clustalw_cline = ClustalwCommandline(cmd = self.clustalw_path, infile=in_file, outfile=out_file, align=True, outorder="ALIGNED", convert=True, output="pir")
            a, b = Clustalw_cline()
        elif (self.comparison == 'muscle'):
            out_file1 = out_file[:-4] + '.aln'
            ml4 = self.muscle_path + ' -in ' + in_file + ' -out ' + out_file1# -clw
            d = os.system(ml4)
            ml5 = hmmbuild + ' ./out_hmm/' + name0 + '.hmm ' + out_file1
            d = os.system(ml5)
        elif self.comparison == 'mafft':
            mafft_cline = MafftCommandline(
                cmd = self.mafft_path, input=in_file, auto=True)
            stdout, stderr = mafft_cline()
            align = AlignIO.read(StringIO(stdout), "fasta")
            AlignIO.write(align, out_file , "fasta")

        os.remove ('one.pep')
        if (os.path.exists('one.dnd')):
            os.remove ('one.dnd')
        path0 = os.getcwd()
        os.chdir('./out_hmm')
        m2 = hmmbuild + ' ' + name0 + '.hmm ..//out_aln/' + name0 + '.aln'
        d = os.system(m2)# 格式转换
        if not os.path.exists(name0):
            os.chdir('../out_aln')
            if self.comparison == "clustal":
                self.format_clustal(name0)
            elif self.comparison == "muscle":
                self.format_muscle(name0)
            elif self.comparison == "mafft":
                self.format_muscle(name0)
            os.chdir('../out_hmm')
            m2 = hmmbuild + ' ' + name0 + '.hmm ..//out_aln/' + name0 + '.sto'
            d = os.system(m2)# 格式转换

        os.chdir('..//')
        m3 = hmmsearch + ' --domtblout ./out_list/' + name0 + '.out -E ' + self.e_value2 + ' ./out_hmm/' + name0 + '.hmm ' + self.pep
        d = os.system(m3)# 第二次搜索，生成out文件
        hmmlist = './out_list/' + name0 + '.out'
        list2 = self.readlist(hmmlist,self.e_value2)# 第二次筛选
        print('Number of gene families: ',len(list2))
        peplist = self.readpep()
        curb = 0
        if self.cds != None:
            cdslist = self.readcds()
            curb = 1
        if len(peplist) == 0:
            print('SETP 2 :No data fit the newmodel')
            return 0
        for i in list2:
            if i in peplist.keys():
                seq = peplist[i]
                file = name0 + '.pep'
                pash0 = './out_pep/'
                self.writepep(pash0,i, seq, file)
            if curb == 1:
                if i in cdslist.keys():
                    cdsseq = cdslist[i]
                    file = name0 + '.cds'
                    pash0 = './out_cds/'
                    self.writepep(pash0,i, cdsseq, file)
        return 1
    def changefile(file,list, hmmpath):
        lix = []
        for i in list:
            name = str(i) + '.hmm'
            oldname = str(i) + '.txt'
            d = os.system("hmmbuild %s %s" % (name, oldname))
            lix.append(str(i))
        return lix

    def readpwd(self, path):
        filelist = []
        path_list=os.listdir(path)
        path_list.sort() #对读取的路径进行排序
        for filename in path_list:
            name = os.path.join(path,filename)
            filelist.append(name[:-4])
        return filelist
    def run(self):
        if os.path.isdir('./out_hmm') and os.path.isdir('./out_cds') and os.path.isdir('./out_pep') and os.path.isdir('./out_list') and os.path.isdir('./out_aln'):
            pass
        else:
            d = os.mkdir("out_hmm")
            d = os.mkdir("out_cds")
            d = os.mkdir("out_pep")
            d = os.mkdir("out_list")
            d = os.mkdir("out_aln")
            print('successfully mkdir')
        if platform.system() == 'Windows':
            hmmpath = self.hmmmoldpath.replace("/", "\\")
        else:
            hmmpath = self.hmmmoldpath
        hmmlistname = self.readpwd(hmmpath)
        if self.format_conversion == 'True':
            hmmlistname = self.changefile(hmmlistname, hmmpath)
        else:
            pass
        for i in hmmlistname:# 遍历模型文件
            i = i + '.hmm'
            x = self.runhmm(i, hmmpath)
            if x == 0:
                continue