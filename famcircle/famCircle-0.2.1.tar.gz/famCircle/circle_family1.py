# -*- coding: UTF-8 -*-
import re
import sys
from math import *
import gc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import *
from matplotlib.patches import Circle, Ellipse
from pylab import *
from collections import Counter
from famCircle.bez import *


class circle_family():
    def __init__(self, options):
    ##### circle parameters
        self.GAP_RATIO = 2 #gaps between chromosome circle, chr:gap = 4: 1
        self.radius = 0.33
        # self.block=0.01 #block scize
        # self.blockthick = 0.004 #0.006
        self.shiftratio = -2.1 # define the distance between overlapping glocks
        self.specieslist = []
        self.iscompletegenome = {}
        self.gene2pos={}
        self.gene2chain = {}
        self.chro2len = {}
        self.otherchrolist = []
        self.genepairsfile_type = 'wgdi'
        self.labels = []
        self.genes = []
        self.genepair2Ks = {}
        self.genepair2Ka = {}
        self.block = '0'
        self.class1 = True
        self.start_list = []
        self.colornum = 1
        self.class1 = True
        # self.color = [ '#a0d8ef', '#c7b370', '#eb6ea5', '#0094c8', '#b8d200', '#00a497'
        #               , '#d9333f', '#3e62ad', '#aacf53', '#f6ad49', '#e9e4d4', '#f39800'
                      # , '#98d98e', '#ffd900', '#68be8d', '#745399', '#028760', '#c0a2c7'],"#eaedf7"
        self.color = ["#2ca9e1","#ffd900","#e2041b","#38b48b","#ea5506","#8f2e14"
                      ,"#b44c97","#f5b1aa","#bce2e8","#82ae46","#824880","#5a544b","#4d4c61"
                      ,"#6f4b3e","#192f60","#2b2b2b","#475950","#727171","#2c4f54","#455765","#432f2f"]
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def readname(self, name):
        name = name.lower()
        if ('^' in name):
            return name
        elif ('g' in name):
            if 'g' not in self.species1+self.species2:
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

    def ksrun(self):
        fpchrolen1 = open(self.lens1,'r', encoding='utf-8')
        fpchrolen2 = open(self.lens2,'r', encoding='utf-8')
        fpgff1 = open(self.gff1,'r', encoding='utf-8')
        fpgff2 = open(self.gff2,'r', encoding='utf-8')
        #### gene block parameters
        figure(1, (8, 8))  ### define the a square, or other rectangle of the figure, if to produce an oval here
        root =axes([0, 0, 1, 1])
        if self.species1 == self.species2:
            lengthset = set()
            for i in [self.species1,self.species2]:
                lengthset.add(len(i))
            # print(lengthset)# 物种名字长度
            chrolist = []
            for row in fpchrolen1:
                chro = row.split('\t')[0]
                for i in lengthset:
                    if (chro[:i] in [self.species1,self.species2]):
                        chrolist.append(chro)
                    else:
                        pass
            fpchrolen1.close()
            # print(chrolist)
            for i in range(len(chrolist)):
                string = chrolist[i]
            #   print string[0:2]
                isnew = 1
                for sp in self.specieslist:
                    if sp == string[0:2]:
                        isnew = 0
                        break
                if isnew==1:
                    self.specieslist.append(string[0:2])
                    if string == string[0:2]:
                        self.iscompletegenome[string[0:2]] = 1
                    else:
                        self.iscompletegenome[string[0:2]] = 0
            # print(self.specieslist)
            # print(self.iscompletegenome)
            ### input chromosome length
            fpchrolen1 = open(self.lens1,'r', encoding='utf-8')
            for row in fpchrolen1:
                if row[0] == '#' or row == '\n':
                    continue
                chro,length = row.split('\t')[0],row.split('\t')[1]
                if len(chro) > 10 :
                    continue
                sp = chro[:2]
                if self.iscompletegenome[sp] == 1 :
                    self.chro2len[chro] = int(length)
                    self.otherchrolist.append(chro)
                else:
                    if chro in chrolist :
                        self.chro2len[chro] = int(length)
                        self.otherchrolist.append(chro)
            fpchrolen1.close()
            # print(self.chro2len,'self.chro2len')
            # print(self.otherchrolist,'self.otherchrolist')
            ### full chro list
            for i in self.otherchrolist:
                self.labels.append(i)
            # print('self.labels',self.labels)
            for row in fpgff1:
                ch, gene, start, end = row.split()[0],row.split()[1],row.split()[2],row.split()[3]
                gene = self.readname(gene)
                start = int(start)
                end = int(end)
                self.gene2pos[gene] = int(start)
                # print(start)
                self.gene2chain[gene] = int((end-start)/abs(end -start))
            fpgff1.close()

        elif self.species1 != self.species2:
            lengthset = set()
            for i in [self.species1,self.species2]:
                lengthset.add(len(i))
            # print(lengthset)# 物种名字长度
            chrolist = []
            for row in fpchrolen1:
                chro = row.split('\t')[0]
                for i in lengthset:
                    if (chro[:i] in [self.species1,self.species2]):
                        chrolist.append(chro)
                    else:
                        pass
            fpchrolen1.close()
            for row in fpchrolen2:
                chro = row.split('\t')[0]
                for i in lengthset:
                    if (chro[:i] in [self.species1,self.species2]):
                        chrolist.append(chro)
                    else:
                        pass
            fpchrolen2.close()
            # print(chrolist)
            for i in range(len(chrolist)):
                string = chrolist[i]
            #   print string[0:2]
                isnew = 1
                for sp in self.specieslist:
                    if sp == string[0:2]:
                        isnew = 0
                        break
                if isnew==1:
                    self.specieslist.append(string[0:2])
                    if string == string[0:2]:
                        self.iscompletegenome[string[0:2]] = 1
                    else:
                        self.iscompletegenome[string[0:2]] = 0
            # print(self.specieslist)
            # print(self.iscompletegenome)
            ### input chromosome length
            fpchrolen1 = open(self.lens1,'r', encoding='utf-8')
            for row in fpchrolen1:
                if row[0] == '#' or row == '\n':
                    continue
                chro,length = row.split('\t')[0],row.split('\t')[1]
                if len(chro) > 10 :
                    continue
                sp = chro[:2]
                if self.iscompletegenome[sp] == 1 :
                    self.chro2len[chro] = int(length)
                    self.otherchrolist.append(chro)
                else:
                    if chro in chrolist :
                        self.chro2len[chro] = int(length)
                        self.otherchrolist.append(chro)
            fpchrolen1.close()
            fpchrolen2 = open(self.lens2,'r', encoding='utf-8')
            for row in fpchrolen2:
                if row[0] == '#' or row == '\n':
                    continue
                chro,length = row.split('\t')[0],row.split('\t')[1]
                if len(chro) > 10 :
                    continue
                sp = chro[:2]
                if self.iscompletegenome[sp] == 1 :
                    self.chro2len[chro] = int(length)
                    self.otherchrolist.append(chro)
                else:
                    if chro in chrolist :
                        self.chro2len[chro] = int(length)
                        self.otherchrolist.append(chro)
            fpchrolen2.close()
            # print(self.chro2len,'self.chro2len')
            # print(self.otherchrolist,'self.otherchrolist')
            ### full chro list
            for i in self.otherchrolist:
                self.labels.append(i)
            # print('self.labels',self.labels)

            for row in fpgff1:
                ch, gene, start, end = row.split()[0],row.split()[1],row.split()[2],row.split()[3]
                gene = self.readname(gene)
                start = int(start)
                end = int(end)
                self.gene2pos[gene] = int(start)
                # print(start)
                self.gene2chain[gene] = int((end-start)/abs(end -start))
            fpgff1.close()

            for row in fpgff2:
                ch, gene, start, end = row.split()[0],row.split()[1],row.split()[2],row.split()[3]
                gene = self.readname(gene)
                start = int(start)
                end = int(end)
                self.gene2pos[gene] = int(start)
                # print(start)
                self.gene2chain[gene] = int((end-start)/abs(end -start))
            fpgff2.close()
        return root

    def rad_to_coord(self, angle, radius):
        return radius*cos(angle), radius*sin(angle)

    def to_radian(self, bp, total):
        # from basepair return as radian
        return radians(bp*360./total)

    def plot_arc(self, start, stop, radius):
        # start, stop measured in radian
        t = arange(start, stop, pi/720.)
        x, y = radius*cos(t), radius*sin(t)
        plot(x, y, '-', color='#ffea00', alpha=.5)# 染色体圆弧#ffea00

    def plot_cap(self, angle, clockwise):
        radius=self.sm_radius
        # angle measured in radian, clockwise is boolean
        if clockwise: 
            t = arange(angle, angle+pi, pi/30.)
        else: 
            t = arange(angle, angle-pi, -pi/30.)
        x, y = radius*cos(t), radius*sin(t)
        middle_r = (self.radius_a+self.radius_b)/2
        x, y = x + middle_r*cos(angle), y + middle_r*sin(angle)
        plot(x, y, '-', color='#ffea00', alpha=.5)# 边缘

    def zj(self):
        fullchrolen = int(pd.DataFrame(self.chro2len.values()).sum())
        chr_number = len(self.labels) # total number of chromosomes
        GAP = fullchrolen/self.GAP_RATIO/chr_number # gap size in base pair
        total_size = fullchrolen + chr_number * GAP # base pairs
        for i in range(chr_number):
            self.start_list.append(0)
        for i in range(1, chr_number):
            self.start_list[i] = self.start_list[i-1] + self.chro2len[self.labels[i-1]] + GAP
        stop_list = [(self.start_list[i] + self.chro2len[self.labels[i]]) for i in range(chr_number)]
        return stop_list, total_size, chr_number

    def transform_pt(self, ch, pos, r, total_size):
        rad = self.to_radian(pos + self.start_list[ch], total_size)
        return r*cos(rad), r*sin(rad)

    def transform_pt0(self, ch, pos, r, total_size):
        rad = self.to_radian(pos + self.start_list[ch], total_size)
        return r*cos(rad), r*sin(rad),rad

    def readblast(self):
        one_gene = []
        alphagenepairs = open(self.genepairs, 'r', encoding='utf-8')
        chrnum = []
        if self.genepairsfile_type == 'wgdi':
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
                        id1 = self.readname(id1)
                        id2 = self.readname(id2)
                        if (id1 not in self.gene2pos.keys() or id2 not in self.gene2pos.keys()):
                            continue
                        chro1 = id1.split("^")[0]
                        chro2 = id2.split("^")[0]
                        if (chro1 not in self.labels or chro2 not in self.labels):
                            continue
                        one_gene.append([id1,id2])
                        chr0 = str(id1.split('^')[0])
                        if chr0 not in chrnum:
                            chrnum.append(chr0)
                        else:
                            pass
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
                        id1, id2 = str(lt[2]),str(lt[3])
                        id1 = self.readname(id1)
                        id2 = self.readname(id2)
                        if (id1 not in self.gene2pos.keys() or id2 not in self.gene2pos.keys()):
                            continue
                        chro1 = id1.split("^")[0]
                        chro2 = id2.split("^")[0]
                        if (chro1 not in self.labels or chro2 not in self.labels):
                            continue
                        one_gene.append([id1,id2])
                        chr0 = str(id1.split('^')[0])
                        if chr0 not in chrnum:
                            chrnum.append(chr0)
                        else:
                            pass
                    else:
                        continue
        elif self.genepairsfile_type == 'blast':
            for row in alphagenepairs:
                if (row[0] == '\n'):
                    continue
                elif ('#' not in row):

                    lt = row.strip('\n').split()
                    # print(lt)
                    id1, id2 = str(lt[0]),str(lt[1])
                    id1 = self.readname(id1)
                    id2 = self.readname(id2)
                    if (id1 not in self.gene2pos.keys() or id2 not in self.gene2pos.keys()):
                        continue
                    chro1 = id1.split("^")[0]
                    chro2 = id2.split("^")[0]
                    if (chro1 not in self.labels or chro2 not in self.labels):
                        continue
                    one_gene.append([id1,id2])
                    chr0 = str(id1.split('^')[0])
                    if chr0 not in chrnum:
                        chrnum.append(chr0)
                    else:
                        pass

        self.colornum = len(chrnum)
        alphagenepairs.close()
        blastlist = sorted(one_gene,key=(lambda x:x[0]))
        return blastlist

    def plot_bez_inner(self, p1, p2, cl, total_size,alp):
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
        xt = Bezier(x, t)
        yt = Bezier(y, t)
        plot(xt, yt, '-', color=cl, lw=1.6, alpha = alp)#alpha 

    def run(self):
        self.radius_a = float(self.radius)
        self.radius_b = self.radius_a + 0.005
        self.sm_radius=(self.radius_b-self.radius_a)/2 #telomere capping
        root = self.ksrun()
        stop_list, total_size, chr_number = self.zj()
        ## sort gene according to lacation on circle
        blastlist = self.readblast()
        rowno = 0
        chrlist = []
        # for i in range(3):
        list000 = []
        # list00 = []
        # family_list = open(self.family_list, 'r', encoding='utf-8')
        # for row in family_list:
        #     if row != '\n' and row[0] != '#':
        #         list00.append(row.strip('\n'))
        # list00 = ['lja1^04212','lja2^00910','lja2^04322','lja2^04914','lja4^01025','lja4^02196','lja5^00060','lja7^01239'
        #   ,'lja8^00488','lja8^01183','lja9^02201','lja9^02588']# utg857g00011,utg857g00009,utg857g00008,utg124g00067
        list00 = ['lja1^04212','lja2^00910','lja2^04914','lja5^00060','lja7^01239','lja8^00488','lja8^01183','lja9^02201','lja9^02588']
        for lt in blastlist:
            id1, id2 = str(lt[0]),str(lt[1])
            pos1 = self.gene2pos[id1]
            pos2 = self.gene2pos[id2]
            chro1 = id1.split("^")[0]
            chro2 = id2.split("^")[0]
            sp1 = chro1[0:2]
            sp2 = chro2[0:2]
            if chro1 in chrlist:
                col = self.color[chrlist.index(chro1)]
            else:
                chrlist.append(chro1)
                col = self.color[len(chrlist) - 1]
            order1 = self.labels.index(chro1)
            order2 = self.labels.index(chro2)
            alp = 0.05
            # if id1.split('^')[0] == id2.split('^')[0]:
            #     # self.plot_bez_inner((order1, pos1, self.radius_a), (order2, pos2, self.radius_a), 'y', total_size,alp)
            #     pass
            # else:
            #     self.plot_bez_inner((order1, pos1, self.radius_a*0.95), (order2, pos2, self.radius_a*0.95), col, total_size,alp)
                # pass

            if id1 in list00 and id2 in list00:
                list000.append([id1, id2])
                
                #e9dfe5
            else:
                self.plot_bez_inner((order1, pos1, self.radius_a*0.8), (order2, pos2, self.radius_a*0.8), '#e9dfe5', total_size,alp)
                # self.plot_bez_inner((order1, pos1, self.radius_a*0.95), (order2, pos2, self.radius_a*0.95), '#e2041b', total_size,0.6)
        
        ltx = []
        for lt in list000:
            id1, id2 = str(lt[0]),str(lt[1])
            pos1 = self.gene2pos[id1]
            pos2 = self.gene2pos[id2]
            chro1 = id1.split("^")[0]
            chro2 = id2.split("^")[0]
            sp1 = chro1[0:2]
            sp2 = chro2[0:2]
            if chro1 in chrlist:
                col = self.color[chrlist.index(chro1)]
            else:
                chrlist.append(chro1)
                col = self.color[len(chrlist) - 1]
            order1 = self.labels.index(chro1)
            order2 = self.labels.index(chro2)
            # dict00 = {'lja1^04212':'LjMTP8c','lja2^00910':'LjMTP3','lja2^04322':'LjMTP3','lja2^04914':'LjMTP6','lja4^01025':'LjMTP12'
            #             ,'lja4^02196':'LjMTP8c','lja5^00060':'LjMTP7a','lja7^01239':'LjMTP12','lja8^00488':'LjMTP11','lja8^01183':'LjMTP10'
            #             ,'lja9^02201':'LjMTP7a','lja9^02588':'LjMTP1'}
            dict00 = {'lja1^04212':'LjMTP8c','lja2^00910':'LjMTP3','lja2^04914':'LjMTP6','lja5^00060':'LjMTP7b'
            ,'lja7^01239':'LjMTP12','lja8^00488':'LjMTP11','lja8^01183':'LjMTP10'
            ,'lja9^02201':'LjMTP7a','lja9^02588':'LjMTP1'}

            self.plot_bez_inner((order1, pos1, self.radius_a*0.8), (order2, pos2, self.radius_a*0.8), "#e60033", total_size,1)
            a, b, c = order1, pos1, self.radius_a*0.91
            ex1x, ex1y,rad1 = self.transform_pt0(a, b, c, total_size)
            a, b, c = order2, pos2, self.radius_a*0.91
            ex2x, ex2y,rad2 = self.transform_pt0(a, b, c, total_size)
            # print(rad1,rad2)
            if id1 not in ltx:
                ltx.append(id1)
                if id1 in dict00.keys():
                    name1 = str(dict00[id1])
                else:
                    name1 = '*'
                if name1 == 'LjMTP1':
                    ex1y = ex1y + 0.004
                if name1 == 'LjMTP7a':
                    ex1y = ex1y - 0.004
                text(ex1x, ex1y, name1, horizontalalignment="center", verticalalignment="center", fontsize = 6, color = 'black',rotation=(rad1/(2*pi))*360)
            if id2 not in ltx:
                ltx.append(id2)
                if id1 in dict00.keys():
                    name2 = str(dict00[id2])
                else:
                    name2 = '*'
                if name2 == 'LjMTP1':
                    ex2y = ex2y + 0.004
                if name2 == 'LjMTP7a':
                    ex2y = ex2y - 0.004
                text(ex2x, ex2y, name2, horizontalalignment="center", verticalalignment="center", fontsize = 6, color = 'black',rotation=(rad2/(2*pi))*360)
                #e9dfe5










            rowno = rowno + 1
        # the chromosome layout
        j = 0
        for start, stop in zip(self.start_list, stop_list):
            start, stop = self.to_radian(start, total_size), self.to_radian(stop, total_size)
            # shaft
            self.plot_arc(start, stop, self.radius_a)
            self.plot_arc(start, stop, self.radius_b)
            # telemere capping
            clockwise=False
            self.plot_cap(start, clockwise)
            clockwise=True
            self.plot_cap(stop, clockwise)
            # chromosome self.labels
            label_x, label_y = self.rad_to_coord((start+stop)/2, self.radius_b*1.05)# text
            #print label_x, label_y
            text(label_x, label_y, self.labels[j].replace('lja','Chr'), horizontalalignment="center", verticalalignment="center", fontsize = 6, color = 'black')
            j+=1
        ########
        root.set_xlim(-.8, .8)#-.5, .5
        root.set_ylim(-.8, .8)
        root.set_axis_off()
        savefig(self.savefile, dpi=1000)
        sys.exit(0)
