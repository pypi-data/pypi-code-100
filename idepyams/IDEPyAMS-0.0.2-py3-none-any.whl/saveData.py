#-------------------------------------------------------------------------------
# Name:        Save Data
# Author:      Dhiabi Fathi
# Created:     26/06/2020
# Copyright:   (c) PyAMS 2020
# Licence:     free
#-------------------------------------------------------------------------------


import  pickle
import  PyAMS
from PyAMS import time,freq;
from option import simulationOption;

ListData=[{'Analysis':{} , 'OutPut':[], 'UsedSweep':False},{}]


def AddToData(OutPut,Analysis):
    global ListData,time,freq;
    ListData[0]['OutPut']=OutPut;
    ListData[0]['Analysis']=Analysis;
    if Analysis['mode']=='tran':
        D=ListData[0]['OutPut']
        used=False;
        for i in range(len(D)):
            if type(D[i])!=str:
              used=used or (D[i].name=='Time')
        if not(used):
            D+=[Time]
    if Analysis['mode']=='ac':
        D=ListData[0]['OutPut']
        used=False;
        for i in range(len(D)):
            if type(D[i])!=str:
              used=used or (D[i].name=='Freq')
        if not(used):
            D+=[Freq]
    if Analysis['mode']=='dc':
        P=Analysis["param"]
        D=ListData[0]["OutPut"]
        used=False;
        for i in range(len(D)):
            if type(D[i])!=str:
              used=used or (D[i].name==P.name)
        if not(used):
            D+=[P]


def getData(name):
    global ListData;
    Data=ListData[1];
    return Data[name];





def SaveInData(Simulation,PosList):
    global ListData;
    OutPut=ListData[0]['OutPut']
    Analysis=ListData[0]['Analysis']
    n=PosList+1;

    if len(ListData) < (n+1):
        ListData+=[{}]
    Data=ListData[n];

    for i in range(len(OutPut)):
      Val,Name=Simulation.getoutput_(OutPut[i]);
      if  Name in Data:
        Data[Name]+=[Val]
      else:
        Data[Name]=[Val]
    if Analysis['mode']=='tr':
        a=Data['Time']
        n=len(a)-1
        a[n]=SimulationOption.t0


'''
    Val=Analysis.Val
    Signals=Analysis.ListSignal
    n=len(Signals)
    for i in range(n):
        name,val=Signals[i].name,Signals[i].Val
        if  name in Data:
            Data[name]+=[val]
        else:
            Data[name]=[val]
            Data['Signals']+=[Signals[i]]
'''

def SaveDataToFile(FileName):
        global ListData;
        with open(FileName, "wb") as fp:
             pickle.dump(ListData, fp)

def OpenDataFromFile(FileName):
        with open(FileName, "rb") as fp:
             return pickle.load(fp)

def SaveDataInSignalParam():
    global ListData;
    Out_=ListData[0]['OutPut']
    Data=ListData[1];
    for i in range(len(Out_)):
        if type(Out_[i]).__name__=='signal':
            Out_[i].Data=Data[Out_[i].name]
        elif  type(Out_[i]).__name__=='param':
            Out_[i].Data=Data[Out_[i].name]


class GetData:
     def __init__(self,FileName):
        self.Data=OpenDataFromFile(FileName)
        self.OutPutNames=[]
        self.PosData=1;
        self.UsedSweep=False; #AppPyAMS.Sweep({"param":R2.R,"list":[100,2000,30000,10000000]})
        self.SweepName='';
        self.SweepList=[];
        self.SweepLengthList=-1;

     def GetSweepParam(self):
        Analysis=self.Data[0]['Analysis']
        if 'sweep' in Analysis:
          self.UsedSweep=True;
          Sweep=Analysis['sweep']
          self.SweepName=Sweep['param'].name;
          self.SweepList=Sweep['list'];
          self.SweepLengthList=len(self.SweepList);
        else:
          self.UsedSweep=False;

     def GetNameXByAnalysys(self):
         Analysis=self.Data[0]['Analysis']
         if Analysis["mode_analysis"]=="tr":
            return 'Time';
         elif Analysis["mode_analysis"]=="dc":
            return  Analysis["param"].name
     def GetOutPut(self):
        return self.Data[0]['OutPut']
     def GetUnitsByName(self,Name):
        Out_=self.Data[0]['OutPut'];
        for i in range(len(Out_)):
             if type(Out_[i]).__name__=='signal':
                    if Name==Out_[i].name:
                        return Out_[i].Unit
             elif  type(Out_[i]).__name__=='param':
                    if Name==Out_[i].name:
                        return Out_[i].Unit

        return 'V'

     def ImportValsByName(self,YName,XName):
          self.y=self.Data[self.PosData][YName]
          self.x=self.Data[self.PosData][XName]
          return len(self.x)


     def GetOutPutNames(self):
        Out_=self.Data[0]['OutPut'];
        self.OutPutNames=[]
        for i in range(len(Out_)):
             if type(Out_[i]).__name__=='signal':
                    self.OutPutNames+=[Out_[i].name]
             elif  type(Out_[i]).__name__=='param':
                    self.OutPutNames+=[Out_[i].name]
             else:
                    self.OutPutNames+=[Out_[i]]
        return   len(self.OutPutNames);








