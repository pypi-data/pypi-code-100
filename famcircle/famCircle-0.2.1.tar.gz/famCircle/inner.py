# -*- encoding: utf-8 -*-
'''
@File        :inner.py
@Time        :2021/09/28 11:17:18
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :放射型圈图
'''


import re
import os
import sys
import gc
from math import *
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import *
from pylab import *
from famCircle.bez import *
from matplotlib import gridspec


class inner():
    def __init__(self, options):
    ##### circle parameters
        self.GAP_RATIO = 5 #gaps between chromosome circle, chr:gap = 4: 1
        self.radius = 0.33
        self.a = 12
        self.block = 0
        self.block_scize= 0.008 #block scize
        self.blockthick = 0.007 #0.006
        self.parameter = 'False'
        self.start_list = {}
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def ksrun(self):
        lens,chr_list = read_lens(self.lens)# 染色体字典
        gff = read_gff(self.gff)# 基因字典
        if self.file_type == 'BLAST':# 关系列表
            blast = read_blast0(self.pair_file)
        elif self.file_type == 'WGDI':# 关系列表
            blast = read_WGDI0(self.pair_file,self.block)
        else:
            print('暂不能解析此文件格式')
            exit()
        ks = read_ks0(self.ks)# ks字典
        family = read_family(self.genefamily)# 家族列表

        # for i in gff:
        #     if gff[i]['chr'] not in lens.keys():
        #         gff = gff.pop(i)
        for i in family:# 去除不在染色体上的家族成员
            if i not in gff.keys():
                family.remove(i)
        return lens,chr_list,gff,blast,ks,family

    def rad_to_coord(self, angle, radius):
        return radius*cos(angle), radius*sin(angle)

    def to_deg(self, bp, total):
        # from basepair return as degree
        return bp*360./total

    def to_radian(self, bp, total):
        # from basepair return as radian
        # print ("to_radian", bp, total)
        return radians(bp*360./total)

    def plot_arc(self, start, stop, radius):
        # start, stop measured in radian 染色体
        #print start, stop
        t = arange(start, stop, pi/720.)
        x, y = radius*cos(t), radius*sin(t)
        plot(x, y, "k-",alpha=.5)

    def plot_cap(self, angle, clockwise):
        radius=self.sm_radius
        # angle measured in radian, clockwise is boolean 鸭舌
        if clockwise: 
            t = arange(angle, angle+pi, pi/30.)
        else: 
            t = arange(angle, angle-pi, -pi/30.)
        x, y = radius*cos(t), radius*sin(t)
        middle_r = (self.radius_a+self.radius_b)/2
        x, y = x + middle_r*cos(angle), y + middle_r*sin(angle)
        plot(x, y, "k-", alpha=.5)

    def plot_arc_block(self, start, radius):# block
        t = arange(start, start+self.block_scize, pi/720.)
        x,y = radius * cos(t), radius*sin(t)
        x1, y1 = (radius-self.blockthick) * cos(t), (radius-self.blockthick) * sin(t)
        plot(x, y, "b-", linewidth=3, alpha=0.5)

    def zj(self,lens,chr_list):
        fullchrolen = sum([lens[i]['end'] for i in lens.keys()])
        fullgene = sum([lens[i]['order'] for i in lens.keys()])
        gene_average = int(fullchrolen/fullgene)
        chr_number = len(lens.keys()) # total number of chromosomes
        GAP = fullchrolen/self.GAP_RATIO/chr_number # gap size in base pair
        total_size = fullchrolen + chr_number * GAP # base pairs 
        # print('total_size',total_size)
        for i in chr_list:
            if i == chr_list[0]:
                self.start_list[i] = 0
            else:
                self.start_list[i] = self.start_list[chr_list[chr_list.index(i)-1]] + lens[chr_list[chr_list.index(i)-1]]['end'] + GAP
        return total_size,gene_average


    def transform_deg(self, ch, pos, total_size):
        return self.to_deg(pos + self.start_list[ch], total_size)

    def transform_pt(self, ch, pos, r, total_size):
        # convert chromosome position to axis coords
        rad = self.to_radian(pos + self.start_list[ch], total_size)
        return r*cos(rad), r*sin(rad)

    def transform_pt1(self,ch, pos, r, total_size):
        # convert chromosome position to axis coords
        # print("transform", ch, pos, r)
    #    print "startlist", self.start_list[ch]
        rad = self.to_radian(pos + self.start_list[ch], total_size)
        return r*cos(rad), r*sin(rad),rad

    def transform_pt2(self, rad, r):
        return r*cos(rad), r*sin(rad)

    def plot_bez_inner(self, p1, p2, cl, total_size,lw0):
    #    print "inner"
        a, b, c = p1
        ex1x, ex1y = self.transform_pt(a, b, c, total_size)
        a, b, c = p2
        ex2x, ex2y = self.transform_pt(a, b, c, total_size)
        # Bezier ratio, controls curve, lower ratio => closer to center
        ratio = .5
        x = [ex1x, ex1x*ratio, ex2x*ratio, ex2x]
        y = [ex1y, ex1y*ratio, ex2y*ratio, ex2y]
        step = .01
        t = arange(0, 1+step, step)
        xt = Bezier(x, t)# 贝塞尔曲线
        yt = Bezier(y, t)
        plot(xt, yt, '-', color=cl, lw=lw0, alpha=0.5)#alpha 透明度

    def plot_bez_Ks2(self, rad1, r1, rad2, r2, col, ratio):
        ex1x, ex1y = self.transform_pt2(rad1, r1)
        ex2x, ex2y = self.transform_pt2(rad2, r2)
        # ratio = -0.7#0.5
        sita = pi / 2
        if ex1x != ex2x:
            sita = atan((ex2y-ex1y)/(ex2x-ex1x))
        d = sqrt((ex2x-ex1x)**2+(ex2y-ex1y)**2)
        L = d * ratio
        P1x = ex1x + L*sin(sita)
        P1y = ex1y - L*cos(sita)
        P2x = ex2x + L*sin(sita)
        P2y = ex2y - L*cos(sita)
        step = .01
        t = arange(0, 1+step, step)
        x=[ex1x, P1x, P2x, ex2x]
        y=[ex1y, P1y, P2y, ex2y]
        # print('x,y,t',x,y,t)
        xt = Bezier(x,t)
        yt = Bezier(y,t)
        plot(xt, yt, '-', color = col, lw = 0.7)#0.1

    def cluster0(self,cluster,id1,id2):
        for i in cluster:
            if id1 in i and id2 in i:
                return True
            else:
                continue
        return False

    def clusterx(self,j,lt):
        for i in range(1,int(self.cluster)):
            if j+i in lt:
                return True
        return False

    def run(self):
        self.radius_a =  float(self.radius)
        self.radius_b = self.radius_a + 0.005#.33, .335   # 半径控制参数 
        self.sm_radius=(self.radius_b-self.radius_a)/2 #telomere capping
        if (os.path.exists(self.savecsv)):
            os.remove(self.savecsv)
        lens,chr_list,gff,blast,ks,family = self.ksrun()
        total_size,gene_average = self.zj(lens,chr_list)
        stop_list = {}

        fig = plt.figure(figsize=(float(self.a), 10))
        gs = gridspec.GridSpec(1, 2, width_ratios=[10, 1])
        gs0 = gridspec.GridSpec(1, 2)
        plt.subplot(gs[0])
        for i in self.start_list.keys():
            stop_list[i] = self.start_list[i] + lens[i]['end']
        for i in chr_list:
            start,stop = self.start_list[i],stop_list[i]
            start, stop = self.to_radian(start, total_size), self.to_radian(stop, total_size)
            # shaft
            self.plot_arc(start, stop, self.radius_a)
            self.plot_arc(start, stop, self.radius_b)
            # telemere capping
            clockwise=False
            self.plot_cap(start, clockwise)
            clockwise=True
            # print(start)
            self.plot_cap(stop, clockwise)
            label_x, label_y = self.rad_to_coord((start+stop)/2, self.radius_b*1.07)#1.2
            #print label_x, label_y
            text(label_x, label_y, i, horizontalalignment="center", verticalalignment="center", fontsize = 7, color = 'black')
        # 绘制关系，并查询inner
        if self.relation == 'True':
            if self.parameter == 'True':
                lt01 = []
                for id1 in blast.keys():
                    if id1 in gff.keys():
                        for id2 in blast[id1]:
                            if id2 in gff.keys():
                                pos1,pos2 = gff[id1]['end'],gff[id2]['end']
                                order1,order2 = gff[id1]['order'],gff[id2]['order']
                                chro1,chro2 = gff[id1]['chr'],gff[id2]['chr']
                                if id1 not in family or id2 not in family:
                                    if chro1==chro2 and abs(order1-order2) > 50:
                                        self.plot_bez_inner((chro1, pos1, self.radius_a*0.9), (chro2, pos2, self.radius_a*0.9), "#d4dcda", total_size,0.2)#绘制内部共线性
                                    elif chro1!=chro2:
                                        self.plot_bez_inner((chro1, pos1, self.radius_a*0.9), (chro2, pos2, self.radius_a*0.9), "#d4dcda", total_size,0.2)#绘制内部共线性
                                elif id1 in family and id2 in family:
                                    if chro1==chro2 and abs(order1-order2) > 50:
                                        if str(id1) + '_' + str(id2) in ks.keys():
                                            ks_v = ks[str(id1) + '_' + str(id2)]
                                        elif str(id2) + '_' + str(id1) in ks.keys():
                                            ks_v = ks[str(id2) + '_' + str(id1)]
                                        else:
                                            continue
                                        if ks_v <= float(self.ks_concern.split(',')[0]) or ks_v >= float(self.ks_concern.split(',')[1]):
                                            col =  "#d4dcda"
                                        else:
                                            lt01.append([id1,id2])
                                            continue
                                        self.plot_bez_inner((chro1, pos1, self.radius_a*0.9), (chro2, pos2, self.radius_a*0.9), "#d4dcda", total_size,0.2)#绘制内部共线性
                                    elif chro1!=chro2:
                                        if str(id1) + '_' + str(id2) in ks.keys():
                                            ks_v = ks[str(id1) + '_' + str(id2)]
                                        elif str(id2) + '_' + str(id1) in ks.keys():
                                            ks_v = ks[str(id2) + '_' + str(id1)]
                                        else:
                                            continue
                                        if ks_v <= float(self.ks_concern.split(',')[0]) or ks_v >= float(self.ks_concern.split(',')[1]):
                                            col =  "#d4dcda"
                                        else:
                                            lt01.append([id1,id2])
                                            continue
                                        self.plot_bez_inner((chro1, pos1, self.radius_a*0.9), (chro2, pos2, self.radius_a*0.9), "#d4dcda", total_size,0.2)#绘制内部共线性
                for i in lt01:
                    id1,id2 = i[0],i[1]
                    pos1,pos2 = gff[id1]['end'],gff[id2]['end']
                    order1,order2 = gff[id1]['order'],gff[id2]['order']
                    chro1,chro2 = gff[id1]['chr'],gff[id2]['chr']
                    if str(id1) + '_' + str(id2) in ks.keys():
                        ks_v = ks[str(id1) + '_' + str(id2)]
                    elif str(id2) + '_' + str(id1) in ks.keys():
                        ks_v = ks[str(id2) + '_' + str(id1)]
                    else:
                        continue
                    col = return_col(ks_v,float(self.ks_concern.split(',')[0]),float(self.ks_concern.split(',')[1]))
                    self.plot_bez_inner((chro1, pos1, self.radius_a*0.95), (chro2, pos2, self.radius_a*0.95), col, total_size,1)#绘制内部共线性
            else:
                lt01 = []
                for id1 in blast.keys():
                    if id1 in gff.keys():
                        for id2 in blast[id1]:
                            if id2 in gff.keys():
                                pos1,pos2 = gff[id1]['end'],gff[id2]['end']
                                order1,order2 = gff[id1]['order'],gff[id2]['order']
                                chro1,chro2 = gff[id1]['chr'],gff[id2]['chr']
                                if chro1==chro2 and abs(order1-order2) > 50:
                                    self.plot_bez_inner((chro1, pos1, self.radius_a*0.9), (chro2, pos2, self.radius_a*0.9), "#d4dcda", total_size,0.2)#绘制内部共线性
                                elif chro1!=chro2:
                                    self.plot_bez_inner((chro1, pos1, self.radius_a*0.9), (chro2, pos2, self.radius_a*0.9), "#d4dcda", total_size,0.2)#绘制内部共线性


            # else:
        #     pass
        fam_dic = {}
        for i in family:
            if gff[i]['chr'] not in fam_dic.keys():
                dicx0 = {}
                dicx0[gff[i]['order']] = i
                fam_dic[gff[i]['chr']] = dicx0
            else:
                fam_dic[gff[i]['chr']][gff[i]['order']] = i

        cluster = []# 基因簇
        for i in fam_dic.keys():
            lt = list(fam_dic[i].keys())
            lt.sort()# 升序
            cluster0 = []
            for j in lt:
                if self.clusterx(j,lt):
                    cluster0.append(fam_dic[i][j])
                else:
                    cluster0.append(fam_dic[i][j])
                    cluster.append(cluster0)
                    cluster0 = []
        
        lt = ['chr', 'gene_list']
        with open(self.savecsv, "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file ,delimiter=',')
            writer.writerow(lt)
        fam_clu = {}
        for i in cluster:
            lt = [gff[i[0]]['chr']] + i
            with open(self.savecsv, "a", newline='', encoding='utf-8') as file:
                writer = csv.writer(file ,delimiter=',')
                writer.writerow(lt)
            for j in range(len(i)):
                fam_clu[i[j]] = j
                posi = gff[i[j]]['end'] + self.start_list[gff[i[j]]['chr']]
                start = self.to_radian(posi, total_size)
                self.plot_arc_block(start, self.radius_a - (j+1) * self.blockthick)# 基因

        ratio = 0.5
        for key in ks.keys():
            id1,id2 = key.split('_')[0],key.split('_')[1]
            if id1 in family and id2 in family and self.cluster0(cluster,id1,id2):
                ks_v = ks[key]
                if ks_v >= float(self.ks_concern.split(',')[0]) and ks_v <= float(self.ks_concern.split(',')[1]):
                    col = return_col(ks_v,float(self.ks_concern.split(',')[0]),float(self.ks_concern.split(',')[1]))
                    posi1 = gff[id1]['end'] + self.start_list[gff[id1]['chr']]
                    start1 = self.to_radian(posi1, total_size)
                    posi2 = gff[id2]['end'] + self.start_list[gff[id2]['chr']]
                    start2 = self.to_radian(posi2, total_size)
                    self.plot_bez_Ks2(start1, (self.radius_a - (fam_clu[id1]+1) * self.blockthick), start2, self.radius_a - (fam_clu[id2]+1) * self.blockthick, col, ratio)

        plt.axis('off')
        drawSpec(float(self.ks_concern.split(',')[0]),float(self.ks_concern.split(',')[1]),gs[1])
        savefig(self.savefile, dpi=1000)
        sys.exit(0)