import requests
from suds.client import Client, sudsobject
import clr  # clr是公共运行时环境，这个模块是与C#交互的核心 pip install pythonnet
import sys  # 导入clr时这个模块最好也一起导入，这样就可以用AddReference方法
# import System
import time
import os
import json,base64
from autotk.AutoCoreLite import *

if (os.path.exists("MesApi.dll")):
    # clr.FindAssembly("MesApi.dll")  ## 加载c#dll文件
    clr.AddReference('MesApi')  # DLL名称不带后缀
    from MesApi import *  # 导入命名空间

class Mes:
    def __init__(self, url, station, scanner="",skip=False,conf=None):
        if (os.path.exists("MesApi.dll")):
            self.addon_api = WS()  # 载入命名空间的类 WS()
        self.skip = skip
        if (self.skip):
            logger.warning("[MES]id=0 Skip Connect")
            self.conf=conf
        else:
            self.token,self.host=self._read_token()
            if(self.token):
                self.itemreport={}
                logger.debug("[MES]%s"%self.host)
            else:
                url=url.strip()
                if ("asmx" in url and not "wsdl" in url):
                    url += "?wsdl"
                logger.debug("[MES]%s" % url)
                self.client = Client(url)
                self.ser = self.client.service
            self.station = station.strip()   # 使用配置的station 而没有使用token里面的station？？
            self.scanner = scanner.strip()
            self.MAC=""
            self.IMEI=""
            self.UID=""
            self.SSID=""
            self.PWD=""
    def _token2json(self, token):
        if ("." in token):
            token = token.split('.')[1]
        for i in range(5):
            if (len(token) % 4):
                token += "="
            else:
                break
        _json = json.loads(base64.b64decode(token).decode())
        return _json
    def _read_token(self):
        token=""
        host=""
        if (os.path.exists("token.txt")):
            try:
                with open("token.txt","r") as t:
                    token=t.read()
                    _json=self._token2json(token)
                    host=_json['host']
            except Exception as e:
                logger.critical("[MEStoken]%s" % e)
                return "", ""
        return token,host
    def url_get(self, token, url, Bearer=True):
        try:
            payload = {}
            if (Bearer):
                headers = {'Authorization': 'Bearer %s' % token, 'Content-Type': 'application/json'}
            else:
                headers = {'Authorization': '%s' % token, 'Content-Type': 'application/json'}
            response = requests.request("GET", url, headers=headers, data=payload)
            response_dict = json.loads(response.text)
            return response.text, response_dict
        except Exception as e:
            logger.critical("[MESAPI]%s"%e)
            return "",{}

    def url_put(self, token, url, data={}, Bearer=True):
        try:
            payload = json.dumps(data)
            if (Bearer):
                headers = {'Authorization': 'Bearer %s' % token, 'Content-Type': 'application/json'}
            else:
                headers = {'Authorization': '%s' % token, 'Content-Type': 'application/json'}
            response = requests.request("PUT", url, headers=headers, data=payload)
            response_dict = json.loads(response.text)
            return response.text, response_dict
        except Exception as e:
            logger.critical("[MESAPI]%s"%e)
            return "",{}
    def url_post(self, token, url, dict={}, Bearer=True):
        try:
            payload = json.dumps(dict)
            if (Bearer):
                headers = {'Authorization': 'Bearer %s' % token, 'Content-Type': 'application/json'}
            else:
                headers = {'Authorization': '%s' % token, 'Content-Type': 'application/json'}
            response = requests.request("POST", url, headers=headers, data=payload)
            response_dict = json.loads(response.text)
            return response.text, response_dict
        except Exception as e:
            logger.critical("[MESAPI]%s"%e)
            return "",{}
    def CheckSN(self, sn, station=None):
        sn=sn.strip()
        if (self.skip):
            logger.debug("[MES]CheckSN: %s"%sn)
            return True
        if(self.token):
            sta = station if station else self.station
            url = "%s/factory/mes/station/%s/%s" % (self.host, sn, sta)
            response, response_dict = self.url_get(self.token,url)
            logger.debug("[MES]CheckSN %s"%response)
            if("code" in response_dict):
                return response_dict['code']==0
            return False
        try:
            # CheckSSN_NEW(xs:string strSN, xs:string station, )
            sta = station if station else self.station
            ret = self.ser.CheckSSN_NEW(sn, sta)
            retlist = sudsobject.asdict(ret)["anyType"]
            logger.debug(retlist)  # [result,msg]
            matchresult = "PASS" in retlist[0]
        except:
            return False
        return matchresult

    def Result(self, sn, judge, station=None, Failcode="", Scanner=None):
        sn=sn.strip()
        if (self.skip):
            logger.debug("[MES]Result: %s %s"%(sn,judge))
            return True
        if(self.token):
            url = "%s/factory/mes/station/%s" % (self.host, sn)
            sta = station if station else self.station
            result = "1" if judge else "0"
            logger.debug("[MES]%s"%self.itemreport)
            data_dist={"station":sta,"pass":result,"param":self.itemreport}
            response, response_dict = self.url_put(self.token,url,data_dist)
            logger.debug("[MES]Upload %s"%response)
            if("code" in response_dict):
                return response_dict['code']==0
            return False
        try:
            result = "PASS" if judge else "FAIL"
            sta = station if station else self.station
            sta_oper = Scanner if Scanner else self.scanner
            # SaveSSN_NEW(xs:string strSSN, xs:string strEventPoint, xs:string strIspass, xs:string strFailcode, xs:string strScanner, )
            ret = self.ser.SaveSSN_NEW(sn, sta, result, Failcode, sta_oper)
            retlist = sudsobject.asdict(ret)["anyType"]
            logger.debug(retlist)  # [result,msg] ['PASS', 'SSN:GZ19100043700003,检查OK！']
            matchresult = "PASS" in retlist[0]
        except:
            return False
        return matchresult

    def Uploaditem(self, sn, testitem, testvalue, judge=True, station=None, Scanner=None):
        sn=sn.strip()
        if (self.skip):
            logger.debug("[MES]Uploaditem: %s %s %s"%(sn,testitem,testvalue))
            return True
        if(self.token):
            self.itemreport[testitem]=str(testvalue)
            return True
        try:
            result = "PASS" if judge else "FAIL"
            sta=station if station else self.station
            sta_oper=Scanner if Scanner else self.scanner
            testtime=time.strftime("%Y-%m-%dT%H:%M:%S")
            # SfcTestResult_Upload(xs:string strEventPoint, xs:string strSSN, xs:string testresult, xs:dateTime testtime, xs:string testitem, xs:string testvalue, xs:string strScanner, )
            ret = self.ser.SfcTestResult_Upload(sta, sn, result, testtime, testitem, str(testvalue), sta_oper)
            retlist = sudsobject.asdict(ret)["anyType"]
            logger.debug(retlist)  # [result,msg]
            matchresult = "PASS" in retlist[0]
        except:
            return False
        return matchresult
    def GetSNbyUID(self,uid):
        uid=uid.strip()
        if (self.skip):
            return True
        try:
            ret,sn=self.addon_api.GetKeys(uid,"")
            if(ret==-1):
                logger.warning("[MES]GetKeys函数执行返回-1")
        except Exception as e:
            logger.critical("[MES]GetKeys DLL 调用出错")
            logger.critical(e)
        return sn
    def PrintSN(self,SN:str,MAC:str,IMEI:str):
        SN=SN.strip()
        MAC=MAC.strip()
        IMEI=IMEI.strip()
        try:
            ret,msg=self.addon_api.PrintSN(SN,MAC,IMEI,"")
            if(ret==-1):
                logger.warning("PrintSN函数执行返回-1")
                return False
        except Exception as e:
            logger.critical("PrintSN DLL 调用出错")
            logger.critical(e)
            return False
        return msg
    def GetMac(self,SN:str,mode=1):
        '''
        mode=1 return sn, emac, null
        mode=2 return sn, null, wmac
        mode=3 return sn, emac, wmac
        '''
        sn=SN.strip()
        emac, wmac = "null", "null"
        if (self.skip):
            debugkeys=self.conf.get(sn.lower(),",".join([sn]*3))
            keys=[i.strip() for i in debugkeys.split(",")]
            if(len(keys)==1):
                if (mode == 1):
                    # 使用显示条码从MES读取emac
                    emac = keys[0]
                elif (mode == 2):
                    # 使用显示条码从MES读取wmac
                    wmac = keys[0]
                elif (mode == 3):
                    # 使用显示条码从MES读取emac和wmac
                    emac=keys[0]
            elif(len(keys)==2):
                if (mode == 1):
                    # 使用显示条码从MES读取emac
                    emac = keys[0]
                elif (mode == 2):
                    # 使用显示条码从MES读取wmac
                    wmac = keys[0]
                elif (mode == 3):
                    # 使用显示条码从MES读取emac和wmac
                    emac, wmac=keys[0],keys[1]
        else:
            if (self.token):
                if (mode == 1):
                    url = "%s/factory/mes/snBind/%s/EMAC" % (self.host, sn)
                    response, response_dict = self.url_get(self.token, url)
                    logger.debug("[MES]GetEMAC %s" % response)
                    if("code" in response_dict):
                        if(response_dict["code"]==0 and "body" in response_dict):
                            emac=response_dict["body"]
                            return sn, emac, wmac
                elif (mode == 2):
                    url = "%s/factory/mes/snBind/%s/WMAC" % (self.host, sn)
                    response, response_dict = self.url_get(self.token, url)
                    logger.debug("[MES]GetWMAC %s" % response)
                    if ("code" in response_dict):
                        if (response_dict["code"] == 0 and "body" in response_dict):
                            wmac = response_dict["body"]
                            return sn, emac, wmac
                elif (mode == 3):
                    url = "%s/factory/mes/snBind/%s/EMAC" % (self.host, sn)
                    response, response_dict = self.url_get(self.token, url)
                    logger.debug("[MES]GetEMAC %s" % response)
                    if ("code" in response_dict):
                        if (response_dict["code"] == 0 and "body" in response_dict):
                            emac = response_dict["body"]
                    url = "%s/factory/mes/snBind/%s/WMAC" % (self.host, sn)
                    response, response_dict = self.url_get(self.token, url)
                    logger.debug("[MES]GetWMAC %s" % response)
                    if ("code" in response_dict):
                        if (response_dict["code"] == 0 and "body" in response_dict):
                            wmac = response_dict["body"]
                    return sn, emac, wmac
                else:
                    return sn, emac, wmac
            try:
                ret = self.ser.GetMACadd(sn)
                retlist = sudsobject.asdict(ret)["anyType"]
                logger.debug(retlist)  # [result,emac,wmac]
                matchresult = "PASS" in retlist[0]
                if(matchresult):
                    if (mode == 1):
                         # 使用显示条码从MES读取emac
                        emac = retlist[1]
                    elif (mode == 2):
                         # 使用显示条码从MES读取wmac
                        wmac = retlist[2]
                    elif (mode == 3):
                        # 使用显示条码从MES读取emac和wmac
                        emac, wmac = retlist[1], retlist[2]
                else:
                    logger.error("[MES]GetMac Fail")
            except Exception as e:
                logger.critical("[MES]GetMac Error %s"%e)
        return sn, emac, wmac
    def GetKeys(self,SN:str,keynum=1):
        SN=SN.strip()
        if (self.skip):
            debugkeys=self.conf.get(SN.lower(),",".join([SN]*keynum))
            keys=tuple([i.strip() for i in debugkeys.split(",")[0:keynum]])
            if(len(keys)==1):
                return keys[0]
            return keys
        if(keynum==2):
            try:
                ret, key1, key2 = self.addon_api.GetKeys(SN, "", "")  #
                if (ret == -1):
                    logger.warning("[MES]GetKeys函数执行返回-1")
            except Exception as e:
                logger.critical("[MES]GetKeys DLL 调用出错")
                logger.critical(e)
            return key1.strip(), key2.strip()
        elif(keynum==3):
            try:
                ret,key1, key2 ,key3=self.addon_api.GetKeys(SN,"","","")    #
                if(ret==-1):
                    logger.warning("[MES]GetKeys函数执行返回-1")
            except Exception as e:
                logger.critical("[MES]GetKeys DLL 调用出错")
                logger.critical(e)
            return key1.strip(), key2.strip() ,key3.strip()
        elif(keynum==4):
            try:
                ret,key1, key2 ,key3,key4=self.addon_api.GetKeys(SN,"","","","")    #
                if(ret==-1):
                    logger.warning("[MES]GetKeys函数执行返回-1")
            except Exception as e:
                logger.critical("[MES]GetKeys DLL 调用出错")
                logger.critical(e)
            return key1.strip(), key2.strip() ,key3.strip(),key4.strip()
        elif (keynum == 5):
            try:
                ret,key1, key2 ,key3,key4,key5=self.addon_api.GetKeys(SN,"","","","","")    #
                if(ret==-1):
                    logger.warning("[MES]GetKeys函数执行返回-1")
            except Exception as e:
                logger.critical("[MES]GetKeys DLL 调用出错")
                logger.critical(e)
            return key1.strip(), key2.strip() ,key3.strip(),key4.strip(),key5.strip()
        else:
            try:
                ret,key1=self.addon_api.GetKeys(SN,"")    #
                if(ret==-1):
                    logger.warning("[MES]GetKeys函数执行返回-1")
            except Exception as e:
                logger.critical("[MES]GetKeys DLL 调用出错")
                logger.critical(e)
            return key1.strip()


if __name__ == '__main__':
    mm = Mes("x1213", "1231", True)
    # print(mm.CheckSN("xxxx", "zzz"))
