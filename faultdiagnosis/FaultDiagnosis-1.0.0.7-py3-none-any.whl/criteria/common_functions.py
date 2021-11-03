#common_functions.py

# 한글 폰트 설정
from matplotlib import font_manager, rc

rc('font', family=font_manager.FontProperties(fname="\c:/Windows/Fonts/malgun.ttf").get_name())
fontprop = font_manager.FontProperties(fname="\c:/Windows/Fonts/malgunbd.ttf", size=12)

from sklearn import ensemble
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, roc_curve
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from scipy.stats import wasserstein_distance, energy_distance
from scipy.spatial import distance
from math import sqrt, fabs, exp
import matplotlib.pyplot as plt
import pylab as plot
import numpy as np
import pandas as pd
import joblib
import datetime as dt
import csv
import pymssql
import pandas.io.sql as psql
import pandas as pd
import pyodbc
import sys
sys.path.insert(0,'./')
import mssql_auth
login = mssql_auth.info

import warnings
warnings.filterwarnings(action='ignore')


class Common:
    __host = login["host"]
    __user = login["user"]
    __password = login["passwd"]
    __database = login["database"]
    __charset = login["charset"]
    SiteCode = ""
    NormalData = {}

    def __init__(self, Sitecode):
        self.SiteCode = Sitecode
        Common.SiteCode = Sitecode
        Common.NormalData.values = ["" for i in range(149)]

    # MSSQL 접속
    @classmethod
    def conn(cls):
       return pymssql.connect(cls.__host, cls.__user, cls.__password, cls.__database, charset='UTF8')

    # 냉방, 난방 구분 (T_OPERATING_CONFIG)
    def sitecode(self):
        db = Common.conn()
        cursor = db.cursor()
        cursor.execute("SELECT top 1 ltrim(SiteCode) FROM T_SITE_INFORMATION WHERE OperationYN = 'Y'")

        all_row = cursor.fetchall()
        SiteCode = all_row[0][0]
        cursor.close()
        db.close()

        Common.SiteCode = SiteCode
        return SiteCode


    # 냉방, 난방 구분 (T_OPERATING_CONFIG)
    def air_condition(SiteCode):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  ltrim(ColdStartDate), ltrim(HeatingStartDate), ColdStartHour, ColdEndHour, HeatingStartHour, HeatingEndHour \
                 FROM T_OPERATING_CONFIG \
                WHERE SiteCode = %s "
        val = (SiteCode)
        cursor.execute(sql, val)

        # 실행문 조회
        all_row = cursor.fetchall()

        ColdStartDate = all_row[0][0]
        HeatingStartDate = all_row[0][1]
        ColdStartHour = all_row[0][2]
        ColdEndHour = all_row[0][3]
        HeatingStartHour = all_row[0][4]
        HeatingEndHour = all_row[0][5]

        cursor.close()
        db.close()

        if (ColdStartDate == None and HeatingStartDate == None):
            print("냉방, 난방일자 중 한 개를 입력하십시오")
            AirCondition = '0'
        if (ColdStartDate != None and ColdStartDate != '' and ColdStartDate != '        ' and len(ColdStartDate)==8):
            AirCondition = '1'
        if (HeatingStartDate != None and HeatingStartDate != '' and HeatingStartDate != '        ' and len(HeatingStartDate)==8):
            AirCondition = '2'
        if (ColdStartDate != None and ColdStartDate != '' and ColdStartDate != '        ' and HeatingStartDate != None and HeatingStartDate != '' and HeatingStartDate != '        ' and len(ColdStartDate)==8 and len(HeatingStartDate)==8):
            print("냉방, 난방 일자 모두 유효합니다. 해당 진단 일자만 입력하십시오")
            AirCondition = '0'
        return AirCondition

    # 냉/난방 시작 날짜 (T_OPERATING_CONFIG)
    def start_date(SiteCode):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  ColdStartDate, HeatingStartDate FROM T_OPERATING_CONFIG WHERE SiteCode = %s"
        val = (SiteCode)
        cursor.execute(sql, val)

        # 실행문 조회
        all_row = cursor.fetchall()

        ColdStartDate = all_row[0][0]
        HeatingStartDate = all_row[0][1]

        cursor.close()
        db.close()

        if (ColdStartDate == None and HeatingStartDate == None):
            print("냉방, 난방일자 중 한 개를 입력하십시오")
            return
        if (ColdStartDate != None and ColdStartDate != '' and ColdStartDate != '        ' and len(ColdStartDate)==8):
            startdate = ColdStartDate
        if (HeatingStartDate != None and HeatingStartDate != '' and HeatingStartDate != '        ' and len(HeatingStartDate)==8):
            startdate = HeatingStartDate
        if (ColdStartDate != None and ColdStartDate != '' and ColdStartDate != '        ' and HeatingStartDate != None and HeatingStartDate != '' and HeatingStartDate != '        ' and len(ColdStartDate)==8 and len(HeatingStartDate)==8):
            print("냉방, 난방 일자 모두 유효합니다. 한 가지 진단일자만 입력하십시오")
        #print("startdate:", startdate)
        return startdate

    # 장비기본 정보 조회 (T_AHU_INFO)
    def ahu_info(EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  ColdSupplySetupTemp, HeatSupplySetupTemp, SupplyAirVolume, OutdoorAirVolume, ExhaustAirVolume \
                FROM T_AHU_INFO \
                WHERE EquipmentClassCode = %s \
                  AND EquipmentNo = %d \
                  AND SiteCode = %s \
                  AND BuildingNo = %s AND ZoneNo = %d"
        val = (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo)
        cursor.execute(sql, val)

        # 실행문 조회
        all_row = cursor.fetchall()
        ColdSupplySetupTemp = all_row[0][0]
        HeatSupplySetupTemp = all_row[0][1]
        SupplyAirVolume = all_row[0][2]
        OutdoorAirVolume = all_row[0][3]
        ExhaustAirVolume = all_row[0][4]

        cursor.close()
        db.close()
        return ColdSupplySetupTemp, HeatSupplySetupTemp, SupplyAirVolume, OutdoorAirVolume, ExhaustAirVolume

    # 공조기 유사도 기준 정보 조회 (T_AHU_CRITERIA_SIMILARITY_INFO)
    def T_AHU_CRITERIA_SIMILARITY_INFO(EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, CoolHeatingIndication):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  CvRMSE, WassersteinDistance, EnergyDistance, PolyDegree \
                 FROM T_AHU_CRITERIA_SIMILARITY_INFO \
                WHERE EquipmentClassCode = %s \
                  AND EquipmentNo = %d \
                  AND SiteCode = %s \
                  AND BuildingNo = %s \
                  AND ZoneNo = %d \
                  AND CoolHeatingIndication = %s"
        val = (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, CoolHeatingIndication)
        cursor.execute(sql, val)

        # 실행문 조회
        all_row = cursor.fetchall()

        if (cursor.rowcount > 0):
            CvRMSE = all_row[0][0]
            WassersteinDistance = all_row[0][1]
            EnergyDistance = all_row[0][2]
            PolyDegree = all_row[0][3]

        if (cursor.rowcount == 0):
            print("찾는 데이터가 없습니다!")
        cursor.close()
        db.close()
        return CvRMSE, WassersteinDistance, EnergyDistance, PolyDegree

    # AHU 센싱정보 조회 (T_AHU_SENSING_INFO)
    def T_AHU_SENSING_INFO(EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  SensingTime, OATemp, SATemp, RATemp, MATemp, SAFlow, OAFlow, RAFlow, SAReh, RAReh, \
                       OADamper, RADamper, EADamper, CoolCVlv, HeatCVlv, SFPower, RFPower \
                 FROM T_AHU_SENSING_INFO \
                WHERE EquipmentClassCode = '" + EquipmentClassCode + "' AND EquipmentNo = EquipmentNo  \
                  AND SiteCode = '" + SiteCode + "' AND BuildingNo = '" + BuildingNo + "' AND ZoneNo = ZoneNo "

        df = pd.read_sql(sql, db)

        cursor.close()
        db.close()
        return df

    # STD 센싱정보 조회
    def T_STD_SENSING_INFO(CoolHeatingIndication):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  OATemp, SATemp, RATemp, MATemp, CoilVlv, SAFlow, OAFlow, OADamper, SFPower, FaultType \
                 FROM T_STD_SENSING_INFO \
                WHERE CoolHeatingIndication = '" + CoolHeatingIndication + "'"
        df = pd.read_sql(sql, db)

        cursor.close()
        db.close()
        return df

    # 운영환경 테이블 조회
    def T_OPERATING_CONFIG(SiteCode):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  ColdStartMonth, ColdEndMonth \
                 FROM T_OPERATING_CONFIG \
                WHERE SiteCode = '" + SiteCode + "'"
        cursor.execute(sql)

        # 실행문 조회
        all_row = cursor.fetchall()
        StartMonth = all_row[0][0]
        EndMonth = all_row[0][1]

        cursor.close()
        db.close()
        return StartMonth, EndMonth

    def recent_normal_data(OperatingDay, AirCondition, SiteCode):

        StartMonth, EndMonth = Common.T_OPERATING_CONFIG(SiteCode)

        db = Common.conn()
        cursor = db.cursor()

        if (AirCondition == "1"):
            sql = "SELECT format(CAST(diagnosisdate AS date), 'yyyyMMdd') \
                     FROM T_AHU_REAL_SIMILARITY_INFO \
                    WHERE FaultYN = 'N' \
                      AND format(CAST(diagnosisdate AS date), 'MM') BETWEEN %s AND %s \
                      AND format(CAST(diagnosisdate AS date), 'yyyyMMdd') BETWEEN \
                          convert(NVARCHAR(8), DATEADD(YEAR, -1, %s), 112) and \
                          convert(NVARCHAR(8), DATEADD(DAY, -1, %s), 112) \
                    GROUP BY format(CAST(diagnosisdate AS date), 'yyyyMMdd')"
            val = (StartMonth, EndMonth, OperatingDay, OperatingDay)

        if (AirCondition == "2"):
            sql = "SELECT date \
                     FROM \
                      (SELECT format(CAST(diagnosisdate AS date), 'yyyyMMdd') as date\
                         FROM T_AHU_REAL_SIMILARITY_INFO \
                        WHERE FaultYN = 'N' \
                          AND format(CAST(diagnosisdate AS date), 'MM') < %s OR format(CAST(diagnosisdate AS date), 'MM') > %s \
                          AND format(CAST(diagnosisdate AS date), 'yyyyMMdd') BETWEEN \
                              convert(NVARCHAR(8), DATEADD(YEAR, -1, %s), 112) and \
                              convert(NVARCHAR(8), DATEADD(DAY, -1, %s), 112) \
                        GROUP BY format(CAST(diagnosisdate AS date), 'yyyyMMdd')) AS REAL_SIMILARITY \
                    WHERE format(CAST(date AS date), 'MM') < %s OR format(CAST(date AS date), 'MM') > %s "
            val = (StartMonth, EndMonth, OperatingDay, OperatingDay, StartMonth, EndMonth)
        cursor.execute(sql, val)

        row = cursor.fetchone()
        i = 0
        while row:
            Common.NormalData[i] = row[0]
            row = cursor.fetchone()
            i = i+1
        normal_data_cnt = i
        cursor.close()
        db.close()
        return normal_data_cnt, Common.NormalData

    def T_AHU_INFO(SiteCode):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  NormalModelYN \
                 FROM T_AHU_INFO \
                WHERE SiteCode = '" + SiteCode + "'"
        cursor.execute(sql)

        # 실행문 조회
        NormalModelYN = cursor.fetchall()
        NormalModelYN = NormalModelYN[0][0]

        cursor.close()
        db.close()
        return NormalModelYN

