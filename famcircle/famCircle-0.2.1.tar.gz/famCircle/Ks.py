# -*- encoding: utf-8 -*-
'''
@File        :Ks.py
@Time        :2021/09/28 11:20:37
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :计算KS
'''


import os
import re
import sys
from io import StringIO
import numpy as np
import pandas as pd
from Bio import AlignIO, SeqIO
from Bio.Align.Applications import MafftCommandline, MuscleCommandline
from Bio.Phylo.PAML import yn00
import famCircle.bez as bez
import time
import copy
# import multiprocessing # Step I : 导入模块
from multiprocessing import cpu_count#读取CPU核心数用于匹配线程数
import gc
import shutil
from multiprocessing import Pool

class Ks():
    def __init__(self, options):
        bez_conf = bez.config()
        self.pair_pep_file = 'pair.pep'
        self.pair_cds_file = 'pair.cds'
        self.prot_align_file = 'prot.aln'
        self.mrtrans = 'pair.mrtrans'
        self.pair_yn = 'pair.yn'
        self.cds_file = 'cds'
        self.pep_file = 'pep'
        self.path0 = os.getcwd()
        for k, v in bez_conf:
            setattr(self, str(k), v)
        for k, v in options:
            setattr(self, str(k), v)
            print(str(k), ' = ', v)
        if hasattr(self, 'process'):
            self.process = int(self.process)
        else:
            if cpu_count() > 16:
                self.process = cpu_count()-10
            else:
                self.process = cpu_count()-1

    def auto_file(self):
        pairs = []
        p = pd.read_csv(self.pairs_file, sep='\n', header=None, nrows=30)
        p = '\n'.join(p[0])
        if 'path length' in p or 'MAXIMUM GAP' in p:
            collinearity = bez.read_colinearscan(self.pairs_file)
            pairs = [[v[0], v[2]] for k in collinearity for v in k[1]]
        elif 'MATCH_SIZE' in p or '## Alignment' in p:
            collinearity = bez.read_mcscanx(self.pairs_file)
            pairs = [[v[0], v[2]] for k in collinearity for v in k[1]]
        elif '# Alignment' in p:
            collinearity = bez.read_coliearity(self.pairs_file)
            pairs = [[v[0], v[2]] for k in collinearity for v in k[1]]
        elif '###' in p:
            collinearity = bez.read_jcvi(self.pairs_file)
            pairs = [[v[0], v[2]] for k in collinearity for v in k[1]]
        elif ',' in p:
            collinearity = pd.read_csv(self.pairs_file, header=None)
            pairs = collinearity.values.tolist()
        else:
            collinearity = pd.read_csv(self.pairs_file, header=None, sep='\t')
            pairs = collinearity.values.tolist()
        df = pd.DataFrame(pairs)
        df = df.drop_duplicates()
        df[0] = df[0].astype(str)
        df[1] = df[1].astype(str)
        df.index = df[0]+','+df[1]
        return df

    def run(self):
        if os.path.exists(self.ks_file):
            ks_file = open(self.ks_file, 'a+')
        else:
            ks_file = open(self.ks_file, 'w')
            ks_file.write(
                '\t'.join(['id1', 'id2', 'ka_NG86', 'ks_NG86', 'ka_YN00', 'ks_YN00'])+'\n')
        if os.path.exists("processes"):
            pass
        else:
            os.mkdir("processes")
        df_pairs = self.auto_file()
        m = df_pairs.iloc[:,0].size
        n = int(np.ceil(m / float(self.process)))
        for i in range(self.process):
            if i < self.process-1:
                print(i*n,i*n+n)
            else:
                print(i*n)
        try:
            pool = Pool(self.process)
            for i in range(self.process):
                if i < self.process-1:
                    new_pd = df_pairs[i*n:i*n+n]
                else:
                    new_pd = df_pairs[i*n:]
                if os.path.exists('processes_'+str(i)):
                    pass
                else:
                    os.mkdir('processes_'+str(i))
                pool.apply_async(self.run0, args=(
                    new_pd,i), error_callback=self.print_error)
            pool.close()
            pool.join()
        except:
            pool.terminate()
        # shutil.rmtree('./processes')


    # 多进程错误打印
    def print_error(self,value):
        print("Process pool error, the cause of the error is :", value)

    def run0(self,df_pairs,n):
        print('The No.',n,' begin the process, process number ',os.getpid())
        os.chdir('processes_'+str(n))
        prefix = '../processes/'+str(n)
        cds = SeqIO.to_dict(SeqIO.parse('../'+self.cds_file, "fasta"))
        pep = SeqIO.to_dict(SeqIO.parse('../'+self.pep_file, "fasta"))
        path = os.getcwd()
        if not os.path.exists('../'+self.pep_file):
            bez.cds_to_pep(os.path.join(path, '../'+self.cds_file),
                            os.path.join(path, '../'+self.pep_file))
        df_pairs = df_pairs[(df_pairs[0].isin(cds.keys())) & (df_pairs[1].isin(
            cds.keys())) & (df_pairs[0].isin(pep.keys())) & (df_pairs[1].isin(pep.keys()))]
        pairs = df_pairs[[0, 1]].to_numpy()
        if len(pairs) > 0 and pairs[0][0][:3] == pairs[0][1][:3]:
            allpairs = []
            pair_hash = {}
            for k in pairs:
                if k[0]+','+k[1] in pair_hash or k[1]+','+k[0] in pair_hash:
                    continue
                else:
                    pair_hash[k[0]+','+k[1]] = 1
                    pair_hash[k[1]+','+k[0]] = 1
                    allpairs.append(k)
            pairs = allpairs
        for k in pairs:
            SeqIO.write([cds[k[0]], cds[k[1]]], prefix+self.pair_cds_file, "fasta")
            SeqIO.write([pep[k[0]], pep[k[1]]], prefix+self.pair_pep_file, "fasta")
            self.read_length(prefix)
            kaks = self.pair_kaks(k,prefix)
            if len(kaks) < 4 or len(list(k)) < 2:
                for file in (prefix+self.pair_pep_file, prefix+self.pair_cds_file, prefix+self.mrtrans, prefix+self.pair_yn, prefix+self.prot_align_file, prefix+'2YN.dN', prefix+'2YN.dS', prefix+'2YN.t', prefix+'rst', prefix+'rst1', prefix+'yn00.ctl', prefix+'rub'):
                    try:
                        os.remove(file)
                    except OSError:
                        pass
                continue
            ks_file = open('../'+self.ks_file, 'a+')
            ks_file.write('\t'.join([str(i) for i in list(k)+list(kaks)])+'\n')
            ks_file.close()
        for file in (prefix+self.pair_pep_file, prefix+self.pair_cds_file, prefix+self.mrtrans, prefix+self.pair_yn, prefix+self.prot_align_file, prefix+'2YN.dN', prefix+'2YN.dS', prefix+'2YN.t', prefix+'rst', prefix+'rst1', prefix+'yn00.ctl', prefix+'rub'):
            try:
                os.remove(file)
            except OSError:
                pass
        gc.collect()
        os.chdir(self.path0)
        shutil.rmtree('processes_'+str(n))
        print('End of the No.',n,' processes, process number ',os.getpid(),'##########################################################')

    def read_length(self,prefix):
        seq = []
        name = []
        s = ''
        for i in open(prefix+self.pair_pep_file,'r'):
            if i[0] == '>':
                if s != '':
                    seq.append(s)
                name.append(i.strip('\n'))
                s = ''
            else:
                s = s + i.strip('\n')
        if s != '':
            seq.append(s)
            s = ''
        if len(seq[0])%3 != 0 or len(seq[1])%3:
            pass

    def pair_kaks(self, k,prefix):
        self.align(prefix)
        pal = self.pal2nal(prefix)
        if not pal:
            return []
        kaks = self.run_yn00(prefix)
        if kaks == None:
            return []
        kaks_new = [kaks[k[0]][k[1]]['NG86']['dN'], kaks[k[0]][k[1]]['NG86']
                    ['dS'], kaks[k[0]][k[1]]['YN00']['dN'], kaks[k[0]][k[1]]['YN00']['dS']]
        return kaks_new

    def align(self,prefix):
        if self.align_software == 'mafft':
            mafft_cline = MafftCommandline(
                cmd=self.mafft_path, input=self.pair_pep_file, auto=True)
            stdout, stderr = mafft_cline()
            align = AlignIO.read(StringIO(stdout), "fasta")
            AlignIO.write(align, self.prot_align_file, "fasta")
        if self.align_software == 'muscle':
            muscle_cline = MuscleCommandline(
                cmd=self.muscle_path, input=prefix+self.pair_pep_file, out=prefix+self.prot_align_file, seqtype="protein", clwstrict=True)
            stdout, stderr = muscle_cline()

    def pal2nal(self,prefix):
        args = ['perl', self.pal2nal_path, prefix+self.prot_align_file,
                prefix+self.pair_cds_file, '-output paml -nogap', '>'+prefix+self.mrtrans]
        command = ' '.join(args)
        try:
            os.system(command)
        except:
            return False
        return True

    def run_yn00(self,prefix):
        yn = yn00.Yn00()
        yn.alignment = prefix+self.mrtrans
        yn.out_file = prefix+self.pair_yn
        yn.set_options(icode=0, commonf3x4=0, weighting=0, verbose=1)
        try:
            run_result = yn.run(command=self.yn00_path)
        except:
            run_result = None
        return run_result
