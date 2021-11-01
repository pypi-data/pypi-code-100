# -*- encoding: utf-8 -*-
'''
@File        :Ks_block.py
@Time        :2021/09/28 11:20:59
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :block的ks
'''


from scipy.stats.kde import gaussian_kde
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from famCircle.bez import *
import sys
import csv


class Ks_block():
    def __init__(self, options):
        self.vertical = "False"
        self.model = "NG86"
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def readks(self):
        read_ks = {}
        f = open(self.ks, 'r', encoding='utf-8')
        for row in f:
            if row[0] != '#' and row[0] != '\n':
                row = row.strip('\n').split('\t')
                if row[0] != 'id1' and len(row) != 2:
                    pair = str(row[0]) + '_' + str(row[1])
                    if self.model == 'NG86':
                        lt = float(row[3])
                    elif self.model == 'YN00':
                        lt = float(row[5])
                    else:
                        print('未能解析ks文件')
                        exit()
                    if lt <= float(self.area.split(',')[0]) or lt >= float(self.area.split(',')[1]):
                        continue
                    read_ks[pair] = lt
        return read_ks

    def readblast(self):
        one_gene = []
        lt00 = []
        alphagenepairs = open(self.genepairs, 'r', encoding='utf-8')
        if self.genepairsfile_type == 'famCircle':
            for row in alphagenepairs:
                if (row[0] == '\n'):
                    continue
                elif (row[0] == '#'):
                    if len(lt00) == 0:
                        pass
                    else:
                        one_gene.append(lt00)
                        lt00 = []
                    lt = row.strip('\n').split(' ')
                    block = {}
                    for i in lt:
                        if '=' in str(i):
                            lt0 = i.split('=')
                            block[str(lt0[0])] = str(lt0[1])
                    N = int(block['N'])
                    if N >= int(self.block):
                        self.class1 = True
                    else :
                        self.class1 = False
                else:
                    if self.class1:
                        lt = row.strip('\n').split()
                        id1, id2 = str(lt[0]),str(lt[1])
                        lt00.append([id1,id2])
        elif self.genepairsfile_type == 'WGDI':
            for row in alphagenepairs:
                if (row[0] == '\n'):
                    continue
                elif (row[0] == '#'):
                    if len(lt00) == 0:
                        pass
                    else:
                        one_gene.append(lt00)
                        # print(lt00)
                        lt00 = []
                    lt = row.strip('\n').split(' ')
                    block = {}
                    for i in lt:
                        if '=' in str(i):
                            lt0 = i.split('=')
                            block[str(lt0[0])] = str(lt0[1])
                    N = int(block['N'])
                    if N >= int(self.block):
                        self.class1 = True
                    else :
                        self.class1 = False
                else:
                    if self.class1:
                        lt = row.strip('\n').split()
                        id1, id2 = str(lt[0]),str(lt[2])
                        lt00.append([id1,id2])
        elif self.genepairsfile_type == 'ColinearScan':
            for row in alphagenepairs:
                if (row[0] == '\n',row[0] == '+'):
                    continue
                elif (row[:3] == 'the'):
                    if len(lt00) == 0:
                        pass
                    else:
                        one_gene.append(lt00)
                        lt00 = []
                    lt = row.strip('\n').split()
                    N = int(lt[-1])
                    if N >= int(self.block):
                        self.class1 = True
                    else :
                        self.class1 = False
                else:
                    if self.class1:
                        lt = row.strip('\n').split()
                        id1, id2 = str(lt[0]),str(lt[2])
                        lt00.append([id1,id2])
        elif self.genepairsfile_type == 'MCScanX':
            for row in alphagenepairs:
                if (row[0] == '\n'):
                    continue
                elif(row[:12] == '## Alignment'):
                    if len(lt00) == 0:
                        pass
                    else:
                        one_gene.append(lt00)
                        lt00 = []
                    lt = row.strip('\n').split(' ')
                    block = {}
                    for i in lt:
                        if '=' in str(i):
                            lt0 = i.split('=')
                            block[str(lt0[0])] = str(lt0[1])
                    N = int(block['N'])
                    if N >= int(self.block):
                        self.class1 = True
                    else :
                        self.class1 = False
                elif ('#' not in row):
                    if self.class1:
                        lt = row.strip('\n').split()
                        # print(lt)
                        if len(lt) == 5:
                            id1, id2 = str(lt[2]),str(lt[3])
                        elif len(lt) == 4:
                            id1, id2 = str(lt[1]),str(lt[2])
                        elif len(lt) == 6:
                            id1, id2 = str(lt[3]),str(lt[4])
                        else:
                            # print(row)
                            print('Parse error!')
                            exit()
                        lt00.append([id1,id2])
        else:
            print('genepairsfile_type error: File Format not recognized!')
            exit()
        if len(lt0) == 0:
            pass
        else:
            one_gene.append(lt00)
            lt00 = []
        return one_gene

        # 绘制核密度曲线图
    def KdePlot(self,list0):
        vertical = 'False'
        y = list0[0]# 平均数
        x = list0[1]# 中位数x = list(map(int, x))
        plt.figure(figsize=(20,10),dpi=800)
        plt.grid(c='grey',ls='--',linewidth=0.3)
        dist_space = np.linspace(float(self.area.split(',')[0]),float(self.area.split(',')[1]), 500)
        kdemedian = gaussian_kde(y)
        kdemedian.set_bandwidth(bw_method=kdemedian.factor / 3.)
        xx = list(dist_space)[list(kdemedian(dist_space)).index(max(list(kdemedian(dist_space))))]
        xx0 = round(xx,4)
        plt.plot(dist_space, kdemedian(dist_space), color='#00a3af',
                 label='average_KDE_' + str(xx0))

        dist_space = np.linspace(float(self.area.split(',')[0]),float(self.area.split(',')[1]), 500)
        kdemedian = gaussian_kde(x)
        kdemedian.set_bandwidth(bw_method=kdemedian.factor / 3.)
        plt.fill_between(dist_space, y1=0, y2=kdemedian(dist_space), facecolor='#d3381c', alpha=0.5)
        xx = list(dist_space)[list(kdemedian(dist_space)).index(max(list(kdemedian(dist_space))))]
        xx0 = round(xx,4)
        plt.plot(dist_space, kdemedian(dist_space), color='#d3381c',
                 label='median_KED_' + str(xx0))
        plt.legend()
        plt.title('block Ks kernel density estimation')# 设置图片标题
        plt.xlabel('ks')# 设置 x 轴标签
        plt.ylabel('density')# 设置 y 轴标签

    def run(self):
        read_ks = self.readks()
        blast = self.readblast()
        average_list = []
        median_list = []
        for i in blast:
            lt = []
            for j in i:
                if str(j[0]) + '_' + str(j[1]) in read_ks.keys():
                    ks_v = read_ks[str(j[0]) + '_' + str(j[1])]
                elif str(j[1]) + '_' + str(j[0]) in read_ks.keys():
                    ks_v = read_ks[str(j[1]) + '_' + str(j[0])]
                else:
                    continue
                lt.append(ks_v)
            if len(lt) == 0:
                continue
            average_list.append(np.mean(lt))
            median_list.append(np.median(lt))
        ks_list = [average_list,median_list]
        self.KdePlot(ks_list)
        plt.savefig(self.savefile, dpi=1000)# 存储图片
        sys.exit(0)