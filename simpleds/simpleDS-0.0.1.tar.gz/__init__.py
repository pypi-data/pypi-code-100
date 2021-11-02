import pandas as pd
import math
import statistics as st





def nullToMean(df,columnNo):
          
        l=list(df.columns)
        columnName=l[columnNo-1]
        columnList=(df.loc[:,columnName]).tolist()
        
        columnList2=[]
        for i in range(0,len(columnList)):
            if(math.isnan(columnList[i])):
                doNothing=True
            else:
                columnList2.append(columnList[i])
                    
        me=st.mean(columnList2)
        for i in range(0,len(columnList)):
                if(math.isnan(columnList[i])):
                        columnList[i]=me
                        
        df=df.drop([columnName], axis=1)
        df.insert(columnNo-1, columnName, columnList)

        return df 



def nullToMedian(df,columnNo):
           
        l=list(df.columns)
        columnName=l[columnNo-1]
        columnList=(df.loc[:,columnName]).tolist()
        
        columnList2=[]
        for i in range(0,len(columnList)):
                if(math.isnan(columnList[i])):
                    doNothing=True
                else:
                    columnList2.append(columnList[i])
                        
        med=st.median(columnList2)
        for i in range(0,len(columnList)):
                if(math.isnan(columnList[i])):
                        columnList[i]=med
        
                        
        df=df.drop([columnName], axis=1)
        df.insert(columnNo-1, columnName, columnList)

        return df



def nullToMode(df,columnNo):
        
        
        l=list(df.columns)
        columnName=l[columnNo-1]
        columnList=(df.loc[:,columnName]).tolist()
        
        columnList2=[]
        for i in range(0,len(columnList)):
                if(math.isnan(columnList[i])):
                    doNothing=True
                else:
                    columnList2.append(columnList[i])
                        
        med=st.mode(columnList2)
        for i in range(0,len(columnList)):
                if(math.isnan(columnList[i])):
                        columnList[i]=med
        
                        
        df=df.drop([columnName], axis=1)
        df.insert(columnNo-1, columnName, columnList)
        return df 



def Mean(df,columnNo):
        
        
        l=list(df.columns)
        columnName=l[columnNo-1]
        columnList=(df.loc[:,columnName]).tolist()
        
        me=st.mean(columnList)
        
        return me



def Median(df,columnNo):
        
        
        l=list(df.columns)
        columnName=l[columnNo-1]
        columnList=(df.loc[:,columnName]).tolist()
        
        me=st.median(columnList)
        
        return me



def Mode(df,columnNo):
        
        
        l=list(df.columns)
        columnName=l[columnNo-1]
        columnList=(df.loc[:,columnName]).tolist()
        
        me=st.mode(columnList)
        
        return me
        


def Normalize(df):
        
    columnNames=df.columns
    for i in range(0,len(columnNames)):

        columnName=columnNames[i]
        columnList=(df.loc[:,columnName]).tolist()
    
        ma=max(columnList)
        mi=min(columnList)
        
        columnList2=[]
        for j in columnList:
            ans=(j-mi)/(ma-mi)
            columnList2.append(ans)
        
        df=df.drop([columnName], axis=1)
        df.insert(i, columnName, columnList2)
        
    return df