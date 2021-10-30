from nebula.graph import ttypes,GraphService
from nebula.ConnectionPool import ConnectionPool
from nebula.Client import GraphClient
import pandas as pd
import numpy as np
import threading
from functools import wraps
from functools import update_wrapper
from copy import deepcopy
import time
from multiprocessing.dummy import Pool as ThreadPool

class SynSaver_process:
    def __init__(self):
        self.synValList=[]

    def docFunc(self,func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.synValList.append(deepcopy(func(*args, **kwargs)))
        return wrapper
mySynSaver_process=SynSaver_process()

@mySynSaver_process.SynSaver_process
def insertRowProcess(rowObj):
    dataList=[]
    for rowItem in rowObj:
        rowList = []
        for colItem in rowItem.columns:
            if type(colItem.value) == bytes:
                rowList.append(colItem.value.decode("utf8"))
            else:
                rowList.append(colItem.value)
        dataList.append(rowList.copy())
    return dataList

def wrapNebula2Df_process(nebulaObj):
    '''将platoDB查询到的对象转为df'''
    # print(nebulaObj.column_names)
    if nebulaObj.column_names is not None:
        columnList = [colItem.decode("utf8") for colItem in nebulaObj.column_names]
    else:
        return pd.DataFrame([])
    pool = ThreadPool()
    
    dataList = []
    if nebulaObj.rows is not None:
        for rowItem in nebulaObj.rows:
            pool.map(insertRowProcess, rowItem)
            pool.close()
            pool.join()
            # insertThread=threading.Thread(target=insertRowThread,args=[nebulaObj.rows[rowI:rowI+batchSize]])
            # threadList.append(insertThread)
    else:
        return pd.DataFrame([])
    
    
    return pd.DataFrame(dataList, columns=columnList).drop_duplicates()

def wrapNebula2Df_single(nebulaObj):
    '''将platoDB查询到的对象转为df'''
    # print(nebulaObj.column_names)
    if nebulaObj.column_names is not None:
        columnList = [colItem.decode("utf8") for colItem in nebulaObj.column_names]
    else:
        return pd.DataFrame([])
    dataList = []
    if nebulaObj.rows is not None:
        for rowItem in nebulaObj.rows:
            rowList = []
            for colItem in rowItem.columns:
                if type(colItem.value) == bytes:
                    rowList.append(colItem.value.decode("utf8"))
                else:
                    rowList.append(colItem.value)
            dataList.append(rowList.copy())
    else:
        return pd.DataFrame([])
    return pd.DataFrame(dataList, columns=columnList).drop_duplicates()

class SynSaver:
    def __init__(self):
        self.synValList=[]

    def docFunc(self,func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.synValList.append(deepcopy(func(*args, **kwargs)))
        return wrapper
mySynSaver=SynSaver()

def wrapNebula2Df(nebulaObj,batchSize=512):
    '''将platoDB查询到的对象转为df'''
    # print(nebulaObj.column_names)
    totalStart=time.time()
    print(totalStart)
    if nebulaObj.column_names is not None:
        columnList = [colItem.decode("utf8") for colItem in nebulaObj.column_names]
    else:
        return pd.DataFrame([])
    dataList = []
    if nebulaObj.rows is not None:
        threadList=[]
        start=time.time()
        for rowI in range(0,len(nebulaObj.rows),batchSize):
            @mySynSaver.docFunc
            def insertRowThread(rowObj):
                dataList=[]
                for rowItem in rowObj:
                    rowList = []
                    for colItem in rowItem.columns:
                        if type(colItem.value) == bytes:
                            rowList.append(colItem.value.decode("utf8"))
                        else:
                            rowList.append(colItem.value)
                    dataList.append(rowList.copy())
                return dataList
            insertThread=threading.Thread(target=insertRowThread,args=[nebulaObj.rows[rowI:rowI+batchSize]])
            threadList.append(insertThread)
        end=time.time()
        print("thread time1:",end-start)
            
        start=time.time()
        if len(threadList)>0:# 清理剩余线程
            for myThreadItem in threadList:
                myThreadItem.start()
            for myThreadItem in threadList:
                myThreadItem.join()
                threadList.pop(0)
        end=time.time()
        print("thread time2:",end-start)
        
        start=time.time()
        for batchItem in deepcopy(mySynSaver.synValList):
            for rowItem in batchItem:
                dataList.append(rowItem)
        end=time.time()
        print("thread time3:",end-start)
    else:
        return pd.DataFrame([])

    mySynSaver.synValList=[]

    start=time.time()
    returnDf=pd.DataFrame(dataList, columns=columnList).drop_duplicates()
    end=time.time()
    print("total time:",end-totalStart)

    return returnDf

def pdPlatoTypeSame(pdSeries,gType):
    '''pd.DataFrame的series的数据类型是否和gType一致'''
    if gType=="string":
        if pdSeries.dtype==object:
            return True
    elif gType=="int":
        if pdSeries.dtype==np.int64:
            return True
    elif gType=="double":
        if pdSeries.dtype==np.float64:
            return True
    return False

def delVertex(gClient,sysIdList,delRel=True):
    '''（关联）删除节点'''
    if delRel==True:
        relDf=wrapNebula2Df(gClient.execute_query("SHOW EDGES"))["Name"]
        relList=relDf.values.flatten().tolist()
        for relItem in relList:
            for srcSysIdItem in sysIdList:
                relTailSysIdDf=wrapNebula2Df(gClient.execute_query("GO FROM {srcSysId} OVER {edgeName} BIDIRECT YIELD {edgeName}._dst AS tgtSysId".format(
                    srcSysId=srcSysIdItem,
                    edgeName=relItem)))
                if relTailSysIdDf.shape[0]>0:
                    relTailSysIdList=relTailSysIdDf["tgtSysId"].values.flatten().tolist()
                    delOrderGroupStr=",".join(["{}->{}".format(srcSysIdItem,tailSysIdItem) for tailSysIdItem in relTailSysIdList])
                    delReverseGroupStr=",".join(["{}->{}".format(tailSysIdItem,srcSysIdItem) for tailSysIdItem in relTailSysIdList])
                    delGroupStr=",".join([delOrderGroupStr,delReverseGroupStr])
                    gClient.execute_query("DELETE EDGE {} {}".format(relItem,delGroupStr))
    for batchI in range(0,len(sysIdList),50): 
        delVerGroupStr=",".join([str(sysIdItem) for sysIdItem in sysIdList[batchI:batchI+50]])
        delReq=gClient.execute_query("DELETE VERTEX {}".format(delVerGroupStr))
    return delReq
                
def existTag(nodeType,nodeIdAttr,nodeName,gClient):
    '''查看nodeType的nodeIdAttr为nodeName的节点是否在gClient中（gClient提前设定好图数据库）'''
    searchTagDf=wrapNebula2Df(gClient.execute_query("LOOKUP ON {nodeType} WHERE {nodeType}.{nodeIdAttr}=='{nodeName}'|LIMIT 1".format(
        nodeType=nodeType,
        nodeIdAttr=nodeIdAttr,
        nodeName=nodeName
    )))
    if searchTagDf.shape[0]>0:
        return True
    return False