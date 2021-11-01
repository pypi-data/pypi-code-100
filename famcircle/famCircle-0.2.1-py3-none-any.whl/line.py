# -*- encoding: utf-8 -*-
'''
@File        :line.py
@Time        :2021/07/11 12:44:00
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :共线性局部
'''

import csv
import sys
import re
from math import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import *
from matplotlib.patches import Circle, Ellipse, Arc
from pylab import *
from famCircle.bez import *

class line():
    def __init__(self, options):
        self.makers = 200
        class1 = False
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def lower_(self,name):
        name = name.lower()
        return name

    def readgff_(self,file):
        myList = []
        for line in open(file,'r'):
            lt = line.strip('\n').split()
            lt[0],lt[1] = lt[1],lt[0]
            lt[0] = self.lower_(lt[0])
            myList.append(lt)
        matrix_gff0 = pd.DataFrame(data = myList)
        matrix_gff0 = matrix_gff0.set_index(0)
        return matrix_gff0

    def read_csv(self):
        self.chrolist = [self.chr1_name,self.chr2_name]
        gff1 = read_gff(self.gff1)
        gff2 = read_gff(self.gff2)
        gff = dict( gff1, **gff2 )
        print(gff)
        matrix_chr1 = pd.read_csv(self.lens1, sep='\t', header=None, index_col=0)
        length1 = matrix_chr1.loc[self.chr1_name,2]
        matrix_chr2 = pd.read_csv(self.lens2, sep='\t', header=None, index_col=0)
        length2 = matrix_chr2.loc[self.chr2_name,2]
        if length1 >= length2:
            x1 = 0.8
            x2 = length2*(0.8/length1)
            maker_str = True
        else :
            x1 = 0.8
            x2 = length1*(0.8/length2)
            maker_str = False
        maker1 ,maker2 = int(max(length2,length1)/self.makers), int(min(length2,length1)/self.makers)
        chro1 = self.chr1_name
        chro2 = self.chr2_name
        matrix_gff1 = self.readgff_(self.gff1)
        matrix_gff2 = self.readgff_(self.gff2)
        matrix_gff1.groupby(by=0)
        matrix_gff2.groupby(by=0)
        return x1,x2,maker1,maker2,matrix_gff1,matrix_gff2,chro1,chro2,maker_str,length1,length2

    def readblast(self):
        blast_dic = {}
        one_gene = []
        alphagenepairs = open(self.genepairs, 'r', encoding='utf-8')
        if self.genepairsfile_type == 'famCircle':
            for row in alphagenepairs:
                if (row[0] == '\n'):
                    continue
                elif (row[0] == '#'):
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
                        if id1 not in one_gene:
                            one_gene.append(id1)
                            blast_dic[id1] = [id2]
                        else:
                            blast_dic[id1].append(id2)
        elif self.genepairsfile_type == 'WGDI':
            for row in alphagenepairs:
                if (row[0] == '\n'):
                    continue
                elif (row[0] == '#'):
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
                        if id1 not in one_gene:
                            one_gene.append(id1)
                            blast_dic[id1] = [id2]
                        else:
                            blast_dic[id1].append(id2)
        elif self.genepairsfile_type == 'ColinearScan':
            for row in alphagenepairs:
                if (row[0] == '\n',row[0] == '+'):
                    continue
                elif (row[:3] == 'the'):
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
                        if id1 not in one_gene:
                            one_gene.append(id1)
                            blast_dic[id1] = [id2]
                        else:
                            blast_dic[id1].append(id2)
        elif self.genepairsfile_type == 'MCScanX':
            for row in alphagenepairs:
                if (row[0] == '\n'):
                    continue
                elif(row[:12] == '## Alignment'):
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
                            print(row)
                            print('Parse error!')
                            exit()
                        if id1 not in one_gene:
                            one_gene.append(id1)
                            blast_dic[id1] = [id2]
                        else:
                            blast_dic[id1].append(id2)
        elif self.genepairsfile_type == 'BLAST':
            num = 0
            name0_list = []
            for row in alphagenepairs:
                if (row[0] == '\n'):
                    continue
                elif ('#' not in row):
                    lt = row.strip('\n').split()
                    if lt[0] == lt[1]:
                        continue
                    if str(lt[0]) not in name0_list:
                        name0_list.append(str(lt[0]))
                        num = 1
                    else:
                        if num <= int(self.block):
                            pass
                        else:
                            continue
                    id1, id2 = str(lt[0]),str(lt[1])
                    if id1 not in one_gene:
                        one_gene.append(id1)
                        blast_dic[id1] = [id2]
                    else:
                        blast_dic[id1].append(id2)
        else:
            print('genepairsfile_type error: File Format not recognized!')
            exit()
        return blast_dic

    def plot_bez_inner(self, ex1x, ex1y, ex2x, ex2y):
        x = [ex1x, ex1x+((ex2x - ex1x)/3+0.1), ex2x-((ex2x - ex1x)/3+0.1), ex2x]
        y = [ex1y, ex1y+((ex2y - ex1y)/3), ex2y-((ex2y - ex1y)/3), ex2y]
        step = .01
        t = arange(0, 1+step, step)
        xt = self.Bezier(x, t)# 贝塞尔曲线
        yt = self.Bezier(y, t)
        plot(xt, yt, '-', color='#7ebea5', lw=1, alpha=0.3)#alpha 透明度

    def calculate_coef(self,p0, p1, p2, p3):
        c = 3*(p1 - p0)
        b = 3*(p2 - p1) -c
        a = p3 - p0 - c - b
        return c, b, a
    def Bezier(self,plist, t):
        # p0 : origin, p1, p2 :control, p3: destination
        p0, p1, p2, p3 = plist
        # calculates the coefficient values
        c, b, a = self.calculate_coef(p0, p1, p2, p3)
        tsquared = t**2
        tcubic = tsquared*t
        return a*tcubic + b*tsquared + c*t + p0

    def make_plot(self,maker1,maker2,list0,length1,length2,gff,chro1,chro2):
        fig1 = plt.figure(num=1, figsize=(10, 10))  # 确保正方形在屏幕上显示一致，固定figure的长宽相等
        axes1 = fig1.add_subplot(1, 1, 1)
        x1 = 0.8
        x2 = length2*(0.8/length1)
        plt.xlim((0, 1))
        plt.ylim((0, 1))
        self.map1(axes1,maker1,0.1,0.3,x1,'#ffec47')# 长染色体0.8
        self.map1(axes1,maker2,0.1+((0.8-x2)/2),0.65,x2,'#ffec47')# 短染色体
        plt.text(0.45, 0.28, chro1)
        plt.text(0.45, 0.67, chro2)
        plt.axis('off')
        self.pair_index(axes1,maker1,maker2,list0,length1,length2,gff,chro1,chro2,x1,x2)
        plt.savefig(self.savefile,dpi=1000)

    def map1(self,axes1,maker,x,y,x1,color):
        # makers = 15 #标尺
        # x = 0.1 #起始坐标x
        # y = 0.1 #起始坐标y
        # x1 = 0.8#染色体长度
        # color='k'
        lw = 1  #比例线宽
        y1 = 0.001
        w = 0.01
        alpha = 1
        # print(y+w+y1, x, x+x1,y, x, x+x1, lw)
        plt.axhline(y=y, xmin=x, xmax=x+x1, lw=lw, c=color, alpha=alpha)
        plt.axhline(y=y+w+y1, xmin=x, xmax=x+x1, lw=lw, c=color, alpha=alpha)
        for i in range(maker):
            mx = x + ((x1/maker)*i)
            plt.axvline(x=mx, ymin=y, ymax=y+(w/2.5), lw=lw, c=color, alpha=alpha)
        base1 = Arc(xy=(x, y+((w+y1)/2)),    # 椭圆中心，（圆弧是椭圆的一部分而已）
                width=w+y1,    # 长半轴
                height=w+y1,    # 短半轴
                angle=90,    # 椭圆旋转角度（逆时针） 
                theta1=0,    # 圆弧的起点处角度
                theta2=180,    # 圆度的终点处角度
                color=color,
                alpha=alpha,
                linewidth=lw
                )
        base2 = Arc(xy=(x1+x, y+((w+y1)/2)),    # 椭圆中心，（圆弧是椭圆的一部分而已）
                width=w+y1,    # 长半轴
                height=w+y1,    # 短半轴
                angle=-90,    # 椭圆旋转角度（逆时针） 
                theta1=0,    # 圆弧的起点处角度
                theta2=180,    # 圆度的终点处角度
                color=color,
                alpha=alpha,
                linewidth=lw   #线宽像素
                )
        axes1.add_patch(base1)
        axes1.add_patch(base2)
        
    def pair_index(self,axes1,maker1,maker2,list0,length1,length2,gff,chro1,chro2,x1,x2):
        pairs = []
        for i in list0:
            id1,id2 = i[0],i[1]
            if gff[id1]['chr'] == chro1:
                pass
            else:
                id1,id2 = i[1],i[0]
            order1,order2 = gff[id1]['order'],gff[id2]['order'] 
            index1,index2 = 0.1+((order1/length1)*x1),0.1+((0.8-x2)/2)+((order2/length2)*x2)
            self.plot_bez_inner(index2,0.65-0.004,index1,0.3+0.01+0.004)

    def run(self):
        lens1,chrlist1 = read_lens(self.lens1)
        lens2,chrlist2 = read_lens(self.lens2)
        chrlist = chrlist1+chrlist2
        lens = dict( lens1, **lens2)
        gff1 = read_gff(self.gff1)
        gff2 = read_gff(self.gff2)
        gff = dict( gff1, **gff2)
        colineartly = self.readblast()
        list0 = []
        for id1 in colineartly.keys():
            if id1 not in gff.keys() or gff[id1]['chr'] not in lens.keys():
                continue
            for id2 in colineartly[id1]:
                if id2 not in gff.keys() or gff[id1]['chr'] not in lens.keys():
                    continue
                chro1,chro2 = gff[id1]['chr'],gff[id2]['chr']
                if [chro1,chro2] == [self.chr1_name,self.chr2_name] or [chro2,chro1] == [self.chr1_name,self.chr2_name]:
                    list0.append([id1, id2])
        length1,length2 = max([lens[self.chr1_name]['order'],lens[self.chr2_name]['order']]),min([lens[self.chr1_name]['order'],lens[self.chr2_name]['order']])
        if length1 == lens[self.chr1_name]['order']:
            chro1,chro2 = self.chr1_name,self.chr2_name
        else:
            chro1,chro2 = self.chr2_name,self.chr1_name
        maker1,maker2 = 8,int(length2/(length1/8))
        self.make_plot(maker1,maker2,list0,length1,length2,gff,chro1,chro2)
