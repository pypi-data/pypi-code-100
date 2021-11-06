#!/usr/bin/env python
#---------------------------------------------------------------------------
# Copyright 2021 Takafumi Ogawa
# Licensed under the Apache License, Version2.0.
#---------------------------------------------------------------------------
# pydecs-eqcond module
#---------------------------------------------------------------------------
import os,sys
import copy
import numpy as np
from pydecs.reference_phases import ReferencePhases
from pydecs.common import product_local

class EquilibriumConditions:

    def __init__(self,input_params,input_paths,root_outfiles="out"):
        if "output_details" in input_params.keys():
            output_details=input_params["output_details"]
        else:
            output_details=False
        if output_details:
            bool_silent_chempotcalc=False
        else:
            bool_silent_chempotcalc=True
        print(" Reading equilibrium conditions (eq)")
        fnout=root_outfiles+"_parameters_temp_gasP.csv"
        fout_tp=open(fnout,"w")
        ### constructing conditions
        temperatures_list=[]
        if "temperature" in input_params:
            temp_params=input_params["temperature"]
            if "tempK_min" in temp_params:
                temp_min=temp_params["tempK_min"]
            else:
                print(" ERROR(temperatures):: missed tempK_min")
                sys.exit()
            if "tempK_max" in temp_params:
                temp_max=temp_params["tempK_max"]
            else:
                temp_max=temp_min
            if "tempK_num" in temp_params:
                temp_num=temp_params["tempK_num"]
            else:
                temp_num=1
            temperatures_list=np.linspace(temp_min,temp_max,temp_num)
        if len(temperatures_list)!=0:
            str1="   Temperatures: "
            str_out="Temperatures,"
            for t1 in temperatures_list:
                str1+=f"{t1}, "
                str_out+=f"{t1}, "
            print(str1[:-2])
            fout_tp.write(str_out[:-2]+"\n")
        ###############################################
        self.elements_fix_Natoms=[]
        self.Natoms_list=[]
        self.Natoms_chempot_init=[]
        if "fix_Natoms" in input_params:
            params1=input_params["fix_Natoms"]
            for params2 in params1:
                e2=params2["element"]
                if "numCell_min" in params2:
                    nat2_min=params2["numCell_min"]
                else:
                    print(" ERROR(eq.natom_targets):: missed numCell_min for "+e2)
                    sys.exit()
                if "numCell_max" in params2:
                    nat2_max=params2["numCell_max"]
                else:
                    nat2_max=nat2_min
                if "numCell_num" in params2:
                    nat2_num=params2["numCell_num"]
                else:
                    nat2_num=1
                if "numCell_log" in params2:
                    nat2_log=params2["numCell_log"]
                else:
                    nat2_log=False
                if "chempot_init" in params2:
                    cpinit2=params2["chempot_init"]
                else:
                    print(" ERROR(eq.fix_Natoms):: missed chempot_init for "+e2)
                    sys.exit()
                self.elements_fix_Natoms.append(e2)
                if nat2_log:
                    self.Natoms_list.append(np.logspace(np.log10(nat2_min),np.log10(nat2_max),nat2_num))
                else:
                    self.Natoms_list.append(np.linspace(nat2_min,nat2_max,nat2_num))
                self.Natoms_chempot_init.append(cpinit2)
        if len(self.elements_fix_Natoms)!=0:
            for ie1,e1 in enumerate(self.elements_fix_Natoms):
                str1=f"   fix_Natoms({e1}): "
                for n1 in self.Natoms_list[ie1]:
                    str1+=f"{n1}, "
                print(str1[:-2])
        ###############################################
        self.elements_fix_chempots=[]
        self.chempots_list=[]
        if "fix_chempots" in input_params:
            params1=input_params["fix_chempots"]
            ### reading common-data
            if "elements" in params1:
                self.elements_fix_chempots=params1["elements"]
            else:
                print(" ERROR(eq.fix_chempots):: missed elements")
                sys.exit()
            for e1 in self.elements_fix_chempots:
                for e2 in self.elements_fix_Natoms:
                    if e1==e2:
                        print(f" ERROR(eq):: duplicate elements in fix_chempots and fix_Natoms: {e1}")
                        sys.exit()
            if "lambda_del" in params1:
                lambda_del=params1["lambda_del"]
            else:
                lambda_del=0.1
            str1="   Elements for fix-chempots: "
            for e1 in self.elements_fix_chempots:
                str1+=f"{e1}, "
            print(str1[:-2])
            print("-"*50)
            refPhase=ReferencePhases(self.elements_fix_chempots,input_paths)
            if not "eq_phases" in params1:
                print(" ERROR(eq.fix_chempots):: missed eq_phases")
                sys.exit()
            ### reading eq_phases
            phases_whole_range=[]
            phases_limits={}
            for params2 in params1["eq_phases"]:
                if not "label" in params2:
                    print(" ERROR(eq.fix_chempots.eq_phases):: missed label")
                    sys.exit()
                l1=params2["label"]
                if not "phases" in params2:
                    print(" ERROR(eq.fix_chempots.eq_phases):: missed phases")
                    sys.exit()
                if l1=="whole-range":
                    phases_whole_range=params2["phases"]
                else:
                    phases_limits[l1]=params2["phases"]
            if len(phases_limits)==0:
                phases_limits["whole"]=phases_whole_range
            else:
                for l1,ph_list in phases_limits.items():
                    ph_list.extend(phases_whole_range)
            for l1,ph_list in phases_limits.items():
                str1=f"   Eq-phases ({l1}): "
                for ph1 in ph_list:
                    str1+=f"{ph1}, "
                    if not refPhase.exists(ph1):
                        print(f" ERROR(eq.fix_chempots):: phase not found: {ph1}")
                        sys.exit()
                print(str1[:-2])
                if len(ph_list)!=len(self.elements_fix_chempots):
                    print(f" ERROR(eq.fix_chempots):: #eq_phases({l1}) is not equal to #elements(fix_chempots)")
                    sys.exit()
            ### reading gas_pressures
            gas_pressures={}
            if "gas_pressures" in params1:
                for params2 in params1["gas_pressures"]:
                    if not "label" in params2:
                        print(" ERROR(eq.fix_chempots.gas_pressures):: missed label")
                        sys.exit()
                    if not "pressPa_min" in params2:
                        print(" ERROR(eq.fix_chempots.gas_pressures):: missed pressPa_min")
                        sys.exit()
                    if "scale_log" in params2:
                        scale_log=params2["scale_log"]
                    else:
                        scale_log=True
                    l1=params2["label"]
                    pmin=params2["pressPa_min"]
                    if "pressPa_max" in params2:
                        pmax=params2["pressPa_max"]
                    else:
                        pmax=pmin
                    if "pressPa_num" in params2:
                        pnum=params2["pressPa_num"]
                    else:
                        pnum=1
                    bool_label=False
                    for l2 in phases_whole_range:
                        if l1==l2:
                            bool_label=True
                    for ph1 in phases_limits.values():
                        for l2 in ph1:
                            if l1==l2:
                                bool_label=True
                    if bool_label:
                        if scale_log:
                            gas_pressures[l1]=np.logspace(np.log10(pmin),np.log10(pmax),pnum)
                        else:
                            gas_pressures[l1]=np.linspace(pmin,pmax,pnum)
            for l1,p1_list in gas_pressures.items():
                str1=f"   Pressures ({l1}): "
                str_out=f"Pressures_{l1}, "
                for p1 in p1_list:
                    str1+=f"{p1:7.1e}, "
                    str_out+=f"{p1:20.15f}, "
                print(str1[:-2])
                fout_tp.write(str_out[:-2]+"\n")
            if len(temperatures_list)==0:
                temp_press_prodlist=["NONE"]
                temp_press_params=[]
            else:
                temp_press_prodlist=temperatures_list
                temp_press_params=["T"]
            for l1,p1_list in gas_pressures.items():
                temp_press_prodlist=product_local(temp_press_prodlist,p1_list)
                temp_press_params.append("P_"+l1)
            if isinstance(temp_press_prodlist[0],float):
                tmp1=[]
                for t1 in temp_press_prodlist:
                    tmp1.append([t1])
                temp_press_prodlist=tmp1
            temp_press_list=[]
            for t1 in temp_press_prodlist:
                d1={}
                for it2,t2 in enumerate(t1):
                    d1[temp_press_params[it2]]=t2
                temp_press_list.append(d1)
            fout_tp.close()
            #### Constructing lambda-list
            lambda_list=[]
            if len(phases_limits)==1:
                lambda_list=[{"whole":1.0}]
            elif len(phases_limits)>1:
                lambda_prodlist=[[t1] for t1 in np.arange(0.0,1.0+1.0e-10,lambda_del)]
                lambda_params=[]
                for i1 in range(len(phases_limits)-2):
                    t1=np.arange(0.0,1.0,lambda_del)
                    lambda_prodlist=product_local(lambda_prodlist,t1)
                for l1 in phases_limits.keys():
                    lambda_params.append(l1)
                for ilam1,lam1 in enumerate(lambda_prodlist):
                    d1={}
                    sum2=0.0
                    for it2,lam2 in enumerate(lam1):
                        sum2+=lam2
                    if sum2>1.0:
                        continue
                    lam1.append(1.0-sum2)
                    for it2,lam2 in enumerate(lam1):
                        d1[lambda_params[it2]]=lam2
                    lambda_list.append(d1)
            if len(phases_limits)>0:
                fnout_lam=root_outfiles+"_parameters_lambda.csv"
                fout_lam=open(fnout_lam,"w")
                str_out=""
                for l1 in lambda_list[0].keys():
                    str_out+=f"{l1:^20s}, "
                fout_lam.write(str_out[:-2]+"\n")
                for lam1 in lambda_list:
                    str_out=""
                    for l1,v1 in lam1.items():
                        str_out+=f"{v1:20.15f}, "
                    fout_lam.write(str_out[:-2]+"\n")
                fout_lam.close()
            def make_ph_list(phlist_in):
                phlist_out=[]
                for ph1 in phlist_in:
                    if refPhase.issolid(ph1):
                        phlist_out.append((ph1,0.0))
                    else:
                        for k1,v1 in tp1.items():
                            if k1=="T":
                                continue
                            if k1.split("_")[1].strip()==ph1:
                                phlist_out.append((ph1,v1))
                return phlist_out
            cond_fixchempots_list=[]
            for tp1 in temp_press_list:
                cp_limits={}
                for l1,ph_list in phases_limits.items():
                    phin_list=make_ph_list(ph_list)
                    cp1=refPhase.calc_atomChempots(tp1["T"],phin_list,bool_silent_chempotcalc)
                    cp_limits[l1]=cp1
                for lam1 in lambda_list:
                    cp1={}
                    for e1 in self.elements_fix_chempots:
                        cp2=0.0
                        for l2,coeff2 in lam1.items():
                            cp2+=coeff2*cp_limits[l2][e1]
                        cp1[e1]=cp2
                    tp2=copy.deepcopy(tp1)
                    for e1,cp2 in cp1.items():
                        tp2["chempot_"+e1]=cp2
                    for l2,coeff2 in lam1.items():
                        tp2["lambda_"+l2]=coeff2
                    cond_fixchempots_list.append(tp2)
        #################################################
        ### Constructing fix-Natoms!!!
        if len(self.elements_fix_Natoms)==0:
            Natoms_target_prod_list=[]
        else:
            fnout=root_outfiles+"_parameters_fixNatoms.csv"
            fout_nat=open(fnout,"w")
            str1=""
            if len(self.elements_fix_Natoms)==1:
                Natoms_target_prod_list=[[t1] for t1 in self.Natoms_list[0]] 
            else:
                Natoms_target_prod_list=copy.deepcopy(self.Natoms_list[0])
                for ie1,e1 in enumerate(self.elements_fix_Natoms):
                    str1+=f"{e1} , "
                    if ie1==0:
                        continue
                    Natoms_target_prod_list=product_local(Natoms_target_prod_list,self.Natoms_list[ie1])
            fout_nat.write(str1[:-2]+"\n")
            for nlist1 in Natoms_target_prod_list:
                str1=""
                for n1 in nlist1:
                    str1+=f"{n1} , "
                fout_nat.write(str1[:-2]+"\n")
            fout_nat.close()
        #################################################
        ### Combining the parameters of fix-chempots and fix-Natoms!!!
        self.eq_conditions=[]
        if len(self.elements_fix_Natoms)==0:
            self.eq_conditions=cond_fixchempots_list
        else:
            for cond1 in cond_fixchempots_list:
                for nlist1 in Natoms_target_prod_list:
                    cond2=copy.deepcopy(cond1)
                    cond3_fixNatoms=[]
                    for ie1,e1 in enumerate(self.elements_fix_Natoms):
                        cond4={}
                        cond4["element"]=e1
                        cond4["target_Natoms"]=nlist1[ie1]
                        cond4["chempot_init"]=self.Natoms_chempot_init[ie1]
                        cond3_fixNatoms.append(cond4)
                    if len(cond3_fixNatoms)>0:
                        cond2["fix_Natoms"]=cond3_fixNatoms
                    self.eq_conditions.append(cond2)
        print("-"*100)
        self.id_cond=0

    def __iter__(self):
        return self

    def __next__(self):
        if self.id_cond == len(self.eq_conditions):
            raise StopIteration()
        cond_out=self.eq_conditions[self.id_cond]
        self.id_cond+=1
        return cond_out

    def get_elements(self):
        return self.elements_fix_chempots+self.elements_fix_Natoms

