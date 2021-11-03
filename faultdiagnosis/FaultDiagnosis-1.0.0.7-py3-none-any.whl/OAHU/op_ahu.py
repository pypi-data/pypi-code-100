#op_ahu.py
#import Criteria.common_functions
from Criteria.common_functions import *

from matplotlib import font_manager, rc
rc('font', family=font_manager.FontProperties(fname="\c:/Windows/Fonts/malgun.ttf").get_name())
fontprop = font_manager.FontProperties(fname="\c:/Windows/Fonts/malgunbd.ttf", size=12)

import pandas as pd
import numpy as np
import joblib
from sklearn import ensemble
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, precision_score, recall_score, confusion_matrix
from scipy.stats import wasserstein_distance
from scipy.stats import energy_distance
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import matplotlib.pylab as plot
import pymssql
import datetime as dt
import os.path

import warnings
warnings.filterwarnings('ignore')
#warnings.filterwarnings(action='ignore')

# (3)운용공조기 정상상태 예측 급기팬 전력량 산출(표준 회귀모델에 운용공조기 10일치 정상데이터 사용)
def op_normal_predict(OperatingDate, AirCondition, EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, StartDate, EndDate):

    if (len(AirCondition) != 1 or len(AirCondition) < 1 or AirCondition == ''):
        print('냉난방구분값이 존재하지 않습니다.')
        sys.exit(0)

    fault_data = Common.T_AHU_SENSING_INFO(EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo)
    fault_data['DATE'] = pd.to_datetime(fault_data['SensingTime'].dt.strftime('%Y%m%d'))
    fault_data_len = len(fault_data)

    NoDataCheck = 0
    NormalModelYN = Common.T_AHU_INFO(SiteCode)
    normal_data_cnt, NormalData = Common.recent_normal_data(OperatingDate, AirCondition, SiteCode)
    print("normal_data_cnt ::", normal_data_cnt)

    if (NormalModelYN != "Y"):

        if (normal_data_cnt <= 0):
            if (fault_data_len <= 10):
                print("고장진단을 실행하기 위한 일정 수준의 데이터가 없어서 프로그램을 종료합니다.!!! :" )
                NoDataCheck = 1
            else:
                fault_data = fault_data.query(StartDate + '<= DATE <=' + EndDate)
                print("10일 간의 정상 유형 데이터로 최적 다항 회귀 모델을 생성합니다.!!! :" )

        if (normal_data_cnt >= 1):
            i = 0
            fault_data_all = pd.DataFrame(index=range(0,0),columns=['SensingTime', 'OATemp', 'SATemp', 'RATemp', 'MATemp',
                    'SAFlow', 'OAFlow', 'RAFlow', 'SAReh', 'RAReh','OADamper', 'RADamper', 'EADamper', 'CoolCVlv', 'HeatCVlv', 'SFPower', 'RFPower', 'DATE'])

            while i < normal_data_cnt:
                fault_data_one = fault_data[fault_data['DATE']==NormalData[i]]
                fault_data_all = pd.concat([fault_data_all, fault_data_one])
                i = i+1

            print("f'운용공조기 정상유형 데이터로 최적 다항 회귀 모델을 생성합니다.")
            fault_data = fault_data_all

    ### 공조기 기본정보 테이블에서 읽어와서 셋팅
    sa_set_temp_c, sa_set_temp_h, sa_flow, oa_flow, ea_flow = Common.ahu_info(EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo)
    print("ahu_info :", sa_set_temp_c, sa_set_temp_h, sa_flow, oa_flow, ea_flow)

    if (AirCondition == "1"):
        sa_set_temp = sa_set_temp_c

    if (AirCondition == "2"):
        sa_set_temp = sa_set_temp_h

    sa_flow_rating = sa_flow
    oa_flow_rating = oa_flow
    ea_flow_rating = ea_flow
    ra_flow_rating = sa_flow_rating - oa_flow_rating + ea_flow_rating

    fault_data['OATemp'] = fault_data['OATemp'] / sa_set_temp
    fault_data['SATemp'] = fault_data['SATemp'] / sa_set_temp
    fault_data['RATemp'] = fault_data['RATemp'] / sa_set_temp
    fault_data['MATemp'] = fault_data['MATemp'] / sa_set_temp
    fault_data['SAFlow'] = fault_data['SAFlow'] / sa_flow_rating
    fault_data['OAFlow'] = fault_data['OAFlow'] / oa_flow_rating
    fault_data['RAFlow'] = fault_data['RAFlow'] / ra_flow_rating
    fault_data['SAReh'] = fault_data['SAReh'] / 100
    fault_data['RAReh'] = fault_data['RAReh'] / 100
    fault_data['OADamper'] = fault_data['OADamper'] / 100
    fault_data['RADamper'] = fault_data['RADamper'] / 100
    fault_data['EADamper'] = fault_data['EADamper'] / 100
    fault_data['CoolCVlv'] = fault_data['CoolCVlv'] / 100
    fault_data['HeatCVlv'] = fault_data['HeatCVlv'] / 100

    if (AirCondition == "1"):
        columns_customed = ['OATemp', 'SATemp', 'MATemp', 'RATemp', 'CoolCVlv', 'SAFlow', 'OAFlow', 'OADamper',
                            'SFPower']

    if (AirCondition == "2"):
        columns_customed = ['OATemp', 'SATemp', 'MATemp', 'RATemp', 'HeatCVlv', 'SAFlow', 'OAFlow', 'OADamper',
                            'SFPower']

    fault_predict = fault_data[columns_customed]

    print('fault_predict:', len(fault_predict))

    dataset = fault_predict.values
    X_pred1 = dataset[:, 0:-1]
    Y_pred1 = dataset[:, -1]
    predict_len = Y_pred1.size

    if (AirCondition == "1"):
        afaultRFModel = joblib.load("./STD-cooling-regression.pkl")

    if (AirCondition == "2"):
        afaultRFModel = joblib.load("./STD-heating-regression.pkl")

    Y_prediction2 = afaultRFModel.predict(X_pred1).flatten()

    if(NoDataCheck == 1):
        return fault_predict, Y_pred1, Y_prediction2, AirCondition, normal_data_cnt, NoDataCheck

    mbe = (np.sum(Y_prediction2) - np.sum(Y_pred1)) / predict_len
    mae = mean_absolute_error(Y_prediction2, Y_pred1)
    mse = mean_squared_error(Y_prediction2, Y_pred1)
    rmse = np.sqrt(mse)
    mean = np.mean(Y_pred1)
    cvmbe = mbe / np.mean(Y_pred1)
    cvmae = mae / np.mean(Y_pred1)
    cvrmse = rmse / np.mean(Y_pred1)

    # R2
    r2 = r2_score(Y_pred1, Y_prediction2)
    # Wasserstein 거리
    wsd = wasserstein_distance(Y_pred1, Y_prediction2)
    # Energy거리
    cramerd = energy_distance(Y_pred1, Y_prediction2)

    # 출력
    print('예측 Cv(RMSE) % ; ' + str(cvrmse * 100))
    print('와서스타인변동계수;' + str(wsd / mean * 100))
    print('에너지거리변동계수;' + str(cramerd / mean * 100) + '\n')
    print('실측 평균 :       ' + str(mean))
    print('예측 MBE :        ' + str(mbe))
    print('예측 MAE :        ' + str(mae))
    print('예측 MSE :        ' + str(mse))
    print('예측 RMSE :       ' + str(rmse))
    print('예측 R2 % ;       ' + str(r2 * 100))
    print('예측 Cv(MBE) % ;  ' + str(cvmbe * 100))
    print('예측 Cv(MAE) % ;  ' + str(cvmae * 100))
    print('와서스테인거리;   ' + str(wsd))
    print('에너지거리;        ' + str(cramerd))

    plt.figure(figsize=(12, 5))
    plt.plot(np.arange(predict_len), Y_prediction2, 'g', label="예측 급기팬 전력량")
    plt.plot(np.arange(predict_len), Y_pred1, 'b', label="실측 급기팬 전력량")
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plt.legend()
    plt.show()

    for i in range(0, predict_len, 100):
        label = Y_pred1[i]
        prediction = Y_prediction2[i]
        print("실측 {:.3f}     예측 {:.3f}".format(label, prediction))

    return fault_predict, Y_pred1, Y_prediction2, normal_data_cnt, NoDataCheck


# (4) 최적 다항 회귀모델 생성(표준 회귀모델에 운용공조기의 10일치 정상데이터 사용하여 산출된 예측치 사용)
#     운영 공조기 보정 데이터 생성
def op_best_poly_reg_model(fault_predict, Y_pred1, Y_prediction2, AirCondition, EquipmentClassCode, EquipmentNo,
                           SiteCode, BuildingNo, ZoneNo):
    Y_fanpower = fault_predict['SFPower'].values
    print("Y_fanpower:", Y_fanpower)

    size = len(Y_fanpower)
    print('Y_fanpower size:', size)

    rmses = []
    degrees = np.arange(1, 5)
    min_rmse, min_deg = 1e10, 0

    ###------------------------------------------------------------------------------------------
    ### 운용공조기 정상상태 보정 급기팬 전력량 산출
    ### (최적다항 회귀모델에 운용공조기 정상상태 실측 급기팬 전력량을 적용)
    ###------------------------------------------------------------------------------------------

    x_train, x_test, y_train, y_test = train_test_split(Y_pred1.reshape(-1, 1), Y_prediction2, test_size=0.3)

    for deg in degrees:

        # Train features
        poly_features = PolynomialFeatures(degree=deg, include_bias=False)
        x_poly_train = poly_features.fit_transform(x_train)

        # Linear regression
        poly_reg = LinearRegression()
        poly_reg.fit(x_poly_train, y_train)

        # Compare with test data
        x_poly_test = poly_features.fit_transform(x_test)
        poly_predict = poly_reg.predict(x_poly_test)
        poly_mse = mean_squared_error(y_test, poly_predict)
        poly_rmse = np.sqrt(poly_mse)
        rmses.append(poly_rmse)

        print('------------------------------')
        print('deg:', deg)
        print('min_rmse:', min_rmse)
        print('poly_rmse:', poly_rmse)
        print('min_deg:', min_deg)

        # Cross-validation of degree
        if min_rmse > poly_rmse:
            min_rmse = poly_rmse
            best_poly_reg = poly_reg
            min_deg = deg

        print('min_deg:', min_deg)

    # 모델 저장하기
    # (4) 최적 다항 회귀모델 저장
    if (AirCondition == '1'):
        joblib.dump(best_poly_reg, "./STD-cooling-polynomial.pkl")

    if (AirCondition == '2'):
        joblib.dump(best_poly_reg, "./STD-heating-polynomial.pkl")

    # Plot and present results
    coef = best_poly_reg.coef_
    print('Best degree {} with RMSE {}, Coefficient id {}'.format(min_deg, min_rmse, coef))

    fig = plot.figure()
    plt.plot(degrees, rmses)
    plt.yscale('log')
    plt.xlabel('Degree')
    plt.ylabel('RMSE')

    # (5) 운용공조기 정상상태 보정 급기팬 전력량 산출
    plt.figure(figsize=(12, 5))
    plt.plot(y_test, 'b', label="기존 예측 급기팬 전력량")
    plt.plot(poly_predict, 'g', label="기존 실측에 대한 예측 급기팬 전력량")
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plt.legend()
    plt.show()

    best_poly_features = PolynomialFeatures(degree=min_deg, include_bias=False)
    Y_poly_pred = best_poly_features.fit_transform(Y_pred1.reshape(-1, 1))
    Y_fanpower = best_poly_features.fit_transform(Y_fanpower.reshape(-1, 1))

    # fault new data 저장
    # 정상 유형 보정 급기팬 전력량 (SAFpower2)
    fanpower_adj = pd.DataFrame(best_poly_reg.predict(Y_fanpower))
    #print('fanpower_adj.size:', fanpower_adj.size)

    fault_new_data = fault_predict
    fault_new_data = fault_new_data.reset_index()
    fault_new_data['SFPowerADJ'] = fanpower_adj

    plot.figure(figsize=(12, 5))
    plot.plot(y_test, 'b', label="다항 실측 급기팬 전력량")
    plot.plot(poly_predict, 'r', label="다항 예측 급기팬 전력량")
    plot.plot(Y_pred1, 'c', label="실측 급기팬 전력량")
    plot.plot(fanpower_adj, 'g', label="보정 급기팬 전력량")

    plot.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plot.legend()
    plot.show()

    ###------------------------------------------------------------------------------------------
    ### (6) 운용 공조기 정상 유형 회귀모델 저장 (운용공조기 보정 정상 데이터 10일치 사용)
    ###------------------------------------------------------------------------------------------

    df_fault = fault_new_data
    #print("df_fault 크기", len(df_fault))

    if (AirCondition == "1"):
        columns_customed = ['OATemp', 'SATemp', 'MATemp', 'RATemp', 'CoolCVlv', 'SAFlow', 'OAFlow', 'OADamper',
                            'SFPowerADJ']

    if (AirCondition == "2"):
        columns_customed = ['OATemp', 'SATemp', 'MATemp', 'RATemp', 'HeatCVlv', 'SAFlow', 'OAFlow', 'OADamper',
                            'SFPowerADJ']

    df_fault = df_fault[columns_customed]
    faultNames = np.array(df_fault.keys())

    dataset = df_fault.values
    X = dataset[:, 0:-1]
    Y = dataset[:, -1]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

    # train random forest at a range of ensemble sizes in order to see how the mse changes
    iTrees = 500
    depth = None
    maxFeat = 4  # try tweaking
    bfaultRFModel = ensemble.RandomForestRegressor(n_estimators=iTrees, max_depth=depth, max_features=maxFeat,
                                                   oob_score=False, random_state=42, n_jobs=-1)

    bfaultRFModel.fit(X_train, Y_train)

    # 모델 저장하기
    if (AirCondition == '1'):
        joblib.dump(bfaultRFModel, "./AHU-cooling-regression.pkl")

    if (AirCondition == '2'):
        joblib.dump(bfaultRFModel, "./AHU-heating-regression.pkl")

    # Accumulate mse on test set
    # 정상 유형 추정 급기팬 전력량 (SAFpower3)
    # (7) 운용공조기 정상상태 추정 급기팬 전력량 산출(SAFpower3) : Y_prediction
    Y_prediction = bfaultRFModel.predict(X_test)

    test_len = Y_test.size
    print("test_len", test_len)
    mbe = (np.sum(Y_prediction) - np.sum(Y_test)) / test_len
    mae = mean_absolute_error(Y_prediction, Y_test)
    mse = mean_squared_error(Y_prediction, Y_test)
    rmse = np.sqrt(mse)
    mean = np.mean(Y_test)
    cvmbe = mbe / np.mean(Y_test)
    cvmae = mae / np.mean(Y_test)
    cvrmse = rmse / np.mean(Y_test)

    fanpower_capacity = 1

    # R2
    r2 = r2_score(Y_test, Y_prediction)
    # Wasserstein 거리
    wsd = wasserstein_distance(Y_test * fanpower_capacity, Y_prediction * fanpower_capacity)
    # Wasswerstein 거리는 주변분포가 주어져 있을 때, 이 두개의 분포를 주변분포로 하는 결합분포 중에서
    # E를 가장 작게 하는 분포를 골랐을 때, p의 기대값
    # Energy거리
    cramerd = energy_distance(Y_test * fanpower_capacity, Y_prediction * fanpower_capacity)

    s_cvrmse = round(((cvrmse * 100) * 2), 3)
    s_wsd = round((((wsd / mean) * 100) * 2), 4)
    s_cramerd = round((((cramerd / mean) * 100) * 2), 4)

    print('유사도 Cv(RMSE) % ;   ' + str(s_cvrmse))
    print('유사도 와서스타인변동계수; ' + str(s_wsd))
    print('유사도 에너지거리변동계수; ' + str(s_cramerd))

    ### 공조기 유사도 기준 입력
    ### T_AHU_CRITERIA_SIMILARITY_INFO start
    db = Common.conn()
    cursor = db.cursor()

    if (AirCondition == '1'):
        CoolHeatInd = '1'
    if (AirCondition == '2'):
        CoolHeatInd = '2'

    poly_degree = str(min_deg)
    dt_now = dt.datetime.now()
    sdate = dt_now.strftime("%Y%m%d %H:%M:%S")
    print("sdate:", sdate, min_deg)

    sql = "SELECT COUNT(*) FROM T_AHU_CRITERIA_SIMILARITY_INFO \
            WHERE EquipmentClassCode = %s \
              AND EquipmentNo = %d \
              AND SiteCode = %s \
              AND BuildingNo = %s \
              AND ZoneNo = %d \
              AND CoolHeatingIndication = %s"
    val = (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, CoolHeatInd, s_cvrmse, s_wsd, s_cramerd, poly_degree, sdate)
    cursor.execute(sql, val)

    # 실행문 조회
    all_row = cursor.fetchall()
    count = all_row[0][0]
    #print("count:",count)

    if (count == 0):
        sql = "INSERT INTO T_AHU_CRITERIA_SIMILARITY_INFO (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, CoolHeatingIndication, CvRMSE, WassersteinDistance, EnergyDistance, PolyDegree, SaveTime) VALUES (%s, %d, %s, %s, %d, %s, %d, %d, %d, %d, %s)"
        val = (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, CoolHeatInd, s_cvrmse, s_wsd, s_cramerd, poly_degree, sdate)
        cursor.execute(sql, val)
        db.commit()

    if (count == 1):
        sql = "DELETE FROM T_AHU_CRITERIA_SIMILARITY_INFO \
                WHERE EquipmentClassCode = %s \
                  AND EquipmentNo = %d \
                  AND SiteCode = %s \
                  AND BuildingNo = %s \
                  AND ZoneNo = %d \
                  AND CoolHeatingIndication = %s"
        val = (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, CoolHeatInd)
        cursor.execute(sql, val)
        sql = "INSERT INTO T_AHU_CRITERIA_SIMILARITY_INFO (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, CoolHeatingIndication, CvRMSE, WassersteinDistance, EnergyDistance, PolyDegree, SaveTime) VALUES (%s, %d, %s, %s, %d, %s, %d, %d, %d, %d, %s)"
        val = (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, CoolHeatInd, s_cvrmse, s_wsd, s_cramerd, poly_degree, sdate)
        cursor.execute(sql, val)
        db.commit()
    cursor.close()
    db.close()
    ### T_AHU_CRITERIA_SIMILARITY_INFO end

    # 출력
    print('시험 Cv(RMSE) % ;   ' + str(cvrmse * 100))
    print('와서스타인변동계수; ' + str((wsd / mean) * 100))
    print('에너지거리변동계수; ' + str((cramerd / mean) * 100) + '\n')
    print('행 갯수 :           ' + str(len(df_fault)))
    print('실측 평균 :         ' + str(mean))
    print('시험 MBE :          ' + str(mbe))
    print('시험 MAE :          ' + str(mae))
    print('시험 MSE :          ' + str(mse))
    print('시험 RMSE :         ' + str(rmse))
    print('시험 R2 % ;         ' + str(r2 * 100))
    print('시험 Cv(MBE) % ;    ' + str(cvmbe * 100))
    print('시험 Cv(MAE) % ;    ' + str(cvmae * 100))
    print('와서스타인거리;     ' + str(wsd))
    print('에너지거리;         ' + str(cramerd))

    # normalize by max importance
    featureImportance = bfaultRFModel.feature_importances_
    print('featureImportance:', featureImportance)
    print('featureImportance.max():', featureImportance.max())
    featureImportance = featureImportance / featureImportance.max()
    sorted_idx = np.argsort(featureImportance)
    print('sorted_idx.shape[0]:', sorted_idx.shape[0])
    print('featureImportance:', featureImportance[sorted_idx])
    barPos = np.arange(sorted_idx.shape[0])
    barPos = np.arange(sorted_idx.shape[0]) + .5

    print('faultNames:', faultNames[sorted_idx])
    plot.barh(barPos, featureImportance[sorted_idx], align='center')
    plot.yticks(barPos, faultNames[sorted_idx])
    plot.xlabel('특성 중요도', fontproperties=fontprop)
    plot.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plot.show()

    plot.figure(figsize=(12, 5))
    plot.plot(Y_test, 'b-+', label="실측 급기팬 전력량")
    plot.plot(Y_prediction, 'g--', label="예측 급기팬 전력량")
    plot.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plot.legend()
    plot.show()

    for i in range(test_len):
        label = Y_test[i]
        prediction = Y_prediction[i]
        print("실측:  {:.5f}, 예측: {:.5f}".format(label, prediction))


