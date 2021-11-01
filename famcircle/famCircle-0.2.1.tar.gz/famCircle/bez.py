# -*- encoding: utf-8 -*-
'''
@File        :bez.py
@Time        :2021/09/28 11:26:28
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :None
'''


import configparser
import os
import re
import famCircle
import numpy as np
import pandas as pd
from Bio import Seq, SeqIO, SeqRecord
import codecs
from tqdm import trange
import matplotlib.pyplot as plt
# Bezier functions

def read_lens(lens):
    chr_dic = {}
    chr_list = []
    for i in open(lens, 'r', encoding='utf-8'):
        if i[0] != '#' or i[0] != '\n':
            line = i.strip('\n').split()
            dic0 = {}
            dic0['end'] = int(line[1])
            dic0['order'] = int(line[2])
            chr_dic[line[0]] = dic0
            chr_list.append(line[0])
    return chr_dic,chr_list

def read_gff(gff):
    gene = {}
    gff = open(gff, 'r', encoding='utf-8').readlines()
    for j in range(len(gff)):
        i = gff[j]
        if i[0] != '#' or i[0] != '\n':
            line = i.strip('\n').split()
            dic0 = {}
            dic0['chr'] = line[0]
            dic0['end'] = int(line[2])
            dic0['order'] = int(line[5])
            gene[line[1]] = dic0
    return gene

def read_blast0(blast0):
    pair_dic = {}
    one = []
    list0 = []
    blast = open(blast0, 'r', encoding='utf-8').readlines()
    for j in trange(len(blast)):
        i = blast[j]
        if i[0] != '#' or i[0] != '\n':
            line = i.strip('\n').split()
            if line[0] not in one:
                if len(list0) != 0:
                    pair_dic[line[0]] = list0
                    list0 = []
                one.append(line[0])
                list0.append(line[1])
            else:
                list0.append(line[1])
    if len(list0) != 0:
        pair_dic[line[0]] = list0
        list0 = []
    return pair_dic

def read_ks0(file0):
    ks = {}
    file = open(file0, 'r', encoding='utf-8').readlines()
    for j in trange(len(file)):
        i = file[j]
        if i[0] == '#' or i[0] == '\n':
            continue
        elif 'id1' in i:
            continue
        else:
            line = i.strip('\n').split()
            if len(line) <= 4:
                continue
            ks[str(line[0]) + '_' + str(line[1])] = float(line[3])
    return ks

def read_WGDI0(file0,block):
    blast = {}
    class1 = False
    file = open(file0, 'r', encoding='utf-8').readlines()
    for j in trange(len(file)):
        i = file[j]
        if i[0] == '\n':
            continue
        elif i[0] == '#':
            lt = i.strip('\n').split()
            for x in lt:
                if 'N=' in x:
                    length = x[2:]
            if int(length) < int(block):
                class1 = False
            else:
                class1 = True
        else:
            if class1:
                line = i.strip('\n').split()
                if line[0] not in blast.keys():
                    lt = []
                    lt.append(line[2])
                    blast[line[0]] = lt
                else:
                    blast[line[0]].append(line[2])
    return blast

def read_family(file):
    family = []
    for i in open(file, 'r', encoding='utf-8'):
        if i[0] != '#' or i[0] != '\n':
            line = i.strip('\n').split()
            if line[0] not in family:
                family.append(line[0])
    return family

def read_family1(file):
    family = []
    family_dic = {}
    for i in open(file, 'r', encoding='utf-8'):
        if i[0] != '#' or i[0] != '\n':
            line = i.strip('\n').split()
            if line[0] not in family:
                family.append(line[0])
                if len(line) == 2:
                    family_dic[line[0]] = line[1]
                else:
                    family_dic[line[0]] = '#4d5aaf'
    return family,family_dic

def getRGB(dWave,maxPix=1,gamma=1):
    #dWave为波长；maxPix为最大值；gamma为调教参数
    waveArea = [380,440,490,510,580,645,780]
    minusWave = [0,440,440,510,510,645,780]
    deltWave = [1,60,50,20,70,65,35]
    for p in range(len(waveArea)):
        if dWave<waveArea[p]:
            break
    pVar = abs(minusWave[p]-dWave)/deltWave[p]
    rgbs = [[0,0,0],[pVar,0,1],[0,pVar,1],[0,1,pVar],
            [pVar,1,0],[1,pVar,0],[1,0,0],[0,0,0]]
    #在光谱边缘处颜色变暗
    if (dWave>=380) & (dWave<420):
        alpha = 0.3+0.7*(dWave-380)/(420-380)
    elif (dWave>=420) & (dWave<701):
        alpha = 1.0
    elif (dWave>=701) & (dWave<780):
        alpha = 0.3+0.7*(780-dWave)/(780-700)
    else:
        alpha = 0       #非可见区
    return [maxPix*(c*alpha)**gamma for c in rgbs[p]]

def return_col(ks,min_,max_):
    # ks越小波长越长颜色越偏红，紫短红长
    wavelength = 760-(((ks-min_)/(max_-min_))*(760-400))
    return getRGB(wavelength)

def drawSpec(min_,max_,gs):#min_,max_
    ax1 = plt.subplot(gs)
    #波长越大ks越小
    pic = np.zeros([10,360,3])
    rgb = [getRGB(d) for d in range(400,760)]
    pic = pic+rgb
    pic0 = np.zeros([360,10,3])
    for i in range(10):
        for j in range(360):
            pic0[j][i] = pic[i][j]
    plt.imshow(pic0)
    plt.yticks(range(0,360,50),[str(format(max_ - i*((max_-min_)/8), '.4f')) for i in range(8)])      #y坐标轴ks越小颜色越红
    plt.xticks([])

def readname(name,chrolist):
    name = name.lower()
    chrolist = chrolist.lower()
    if ('^' in name):
        return name
    elif ('g' in name):
        if 'g' not in chrolist:
            name = name.replace('g', '^')
        else :
            lt = name.split('g')
            name = ''
            for i in range(len(lt)):
                if i < len(lt) - 2:
                    name = name + str(lt[i]) + 'g'
                elif i == len(lt) - 2:
                    name = name + str(lt[-2])
                else:
                    name = name + "^" + str(lt[-1])
        return name

def config():
    conf = configparser.ConfigParser()
    conf.read(os.path.join(famCircle.__path__[0], 'conf.ini'))
    return conf.items('ini')

def load_conf(file, section):
    conf = configparser.ConfigParser()
    conf.read(file)
    return conf.items(section)

def read_coliearity0(file,chrolist):
    f = open(file,'r', encoding='utf-8')
    pair_list = []
    for line in f:
        if line[0] == '#':
            continue
        else:
            lt = line.strip('\n').split()
            genepair = ''
            gene1 = readname(str(lt[0]),chrolist)
            gene2 = readname(str(lt[2]),chrolist)
            if gene1 < gene2:
               genepair = gene1 + " " + gene2
            else:
               genepair = gene2 + " " + gene1
            pair_list.append(genepair)
    return pair_list

def read_blast(file,chrolist):
    f = open(file,'r', encoding='utf-8')
    pair_list = []
    for line in f:
        if line[0] == '#':
            continue
        else:
            lt = line.strip('\n').split()
            genepair = ''
            gene1 = readname(str(lt[0]),chrolist)
            gene2 = readname(str(lt[1]),chrolist)
            if gene1 < gene2:
               genepair = gene1 + " " + gene2
            else:
               genepair = gene2 + " " + gene1
            pair_list.append(genepair)
    return pair_list

def calculate_coef(p0, p1, p2, p3):
    c = 3*(p1 - p0)
    b = 3*(p2 - p1) -c
    a = p3 - p0 - c - b
    return c, b, a

def Bezier(plist, t):
    # p0 : origin, p1, p2 :control, p3: destination
    p0, p1, p2, p3 = plist
    # calculates the coefficient values
    c, b, a = calculate_coef(p0, p1, p2, p3)
    tsquared = t**2
    tcubic = tsquared*t
    return a*tcubic + b*tsquared + c*t + p0

def gene_length(gfffile):
    # 读取基因长度，得到平均长度和最小最大长度
    f = open(gfffile,'r', encoding='utf-8')
    genelength = {}
    for row in f:
        if row[0] != '\n' and row[0] != '#':
            row = row.strip('\n').split('\t')
            if str(row[1]) in genelength.keys():
                continue
            if 'chr' == str(row[1])[3:6]:
                continue
            length = abs(int(row[3]) - int(row[2]))
            genelength[str(row[1])] = length
    f.close()
    lt = []
    for i in genelength.values():
        lt.append(i)
    pj = sum(lt)/len(lt)
    return pj

def gene_length_order(lensfile):
    # 读取基因长度，得到平均长度和最小最大长度
    f = open(lensfile,'r', encoding='utf-8')
    gene_sum = 0
    gene_index = 0
    for row in f:
        if row[0] != '\n' and row[0] != '#':
            row = row.strip('\n').split('\t')
            gene_sum = gene_sum + int(row[2])
            gene_index = gene_index + int(row[1])
    f.close()
    pj = gene_index/gene_sum
    return pj

def cds_to_pep(cds_file, pep_file, fmt='fasta'):
    records = list(SeqIO.parse(cds_file, fmt))
    for k in records:
        k.seq = k.seq.translate()
    SeqIO.write(records, pep_file, 'fasta')
    return True

def read_colinearscan(file):
    data, b, flag, num = [], [], 0, 1
    with open(file) as f:
        for line in f.readlines():
            line = line.strip()
            if re.match(r"the", line):
                num = re.search('\d+', line).group()
                b = []
                flag = 1
                continue
            if re.match(r"\>LOCALE", line):
                flag = 0
                p = re.split(':', line)
                if len(b) > 0:
                    data.append([num, b, p[1]])
                b = []
                continue
            if flag == 1:
                a = re.split(r"\s", line)
                b.append(a)
    return data


def read_mcscanx(fn):
    f1 = open(fn)
    data, b = [], []
    flag, num = 0, 0
    for line in f1.readlines():
        line = line.strip()
        if re.match(r"## Alignment", line):
            flag = 1
            if len(b) == 0:
                arr = re.findall(r"[\d+\.]+", line)[0]
                continue
            data.append([num, b, 0])
            b = []
            num = re.findall(r"\d+", line)[0]
            continue
        if flag == 0:
            continue
        a = re.split(r"\:", line)
        c = re.split(r"\s+", a[1])
        b.append([c[1], c[1], c[2], c[2]])
    data.append([num, b, 0])
    return data


def read_jcvi(fn):
    f1 = open(fn)
    data, b = [], []
    num = 1
    for line in f1.readlines():
        line = line.strip()
        if re.match(r"###", line):
            if len(b) == 0:
                continue
            data.append([num, b, 0])
            b = []
            num += 1
            continue
        a = re.split(r"\t", line)
        b.append([a[0], a[0], a[1], a[1]])
    data.append([num, b, 0])
    return data


def read_coliearity(fn):
    f1 = open(fn)
    data, b = [], []
    flag, num = 0, 0
    for line in f1.readlines():
        line = line.strip()
        if re.match(r"# Alignment", line):
            flag = 1
            if len(b) == 0:
                arr = re.findall('[\.\d+]+', line)
                continue
            data.append([arr[0], b, arr[2]])
            b = []
            arr = re.findall('[\.\d+]+', line)
            continue
        if flag == 0:
            continue
        b.append(re.split(r"\s", line))
    data.append([arr[0], b, arr[2]])
    return data

def read_ks(file, col):
    ks = pd.read_csv(file, sep='\t')
    ks.drop_duplicates(subset=['id1', 'id2'], keep='first', inplace=True)
    ks[col] = ks[col].astype(float)
    ks = ks[ks[col] >= 0]
    ks.index = ks['id1']+','+ks['id2']
    return ks[col]
