# fault_detect.py

# 고장 진단용 추정 급기팬 전력량 산출
# 운용공조기 고장진단용 데이터 운용공조기 회기모델에 적용하여
# 유사도 지수 3개를 산출하여 고장진단 실행 여부 조사

from Criteria.common_functions import *

# 한글 폰트 설정
from matplotlib import font_manager, rc
rc('font', family=font_manager.FontProperties(fname="\c:/Windows/Fonts/malgun.ttf").get_name())
fontprop = font_manager.FontProperties(fname="\c:/Windows/Fonts/malgunbd.ttf", size=12)
from sklearn import ensemble
import datetime as dt
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, roc_curve
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import wasserstein_distance,energy_distance
from sklearn.model_selection import train_test_split
import matplotlib.pylab as plot
import pymssql
import warnings
warnings.filterwarnings(action='ignore')
#import matplotlib
#matplotlib.use('Agg')
#import csv


# (10) 고장 진단용 추정 급기팬 전력량 산출
# 운용공조기 고장진단용 데이터 운용공조기 회기모델에 적용하여
# 유사도 지수 3개를 산출하여 고장진단 실행 여부 조사

def fault_detect(OperatingDate, EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, CoolHeatingIndication):
    ###################################################
    ########### 유사도 지수 산출 (날짜별) #############
    ###################################################

    #SiteCode = Common.sitecode(Common.SiteCode)
    AirCondition = Common.air_condition(SiteCode)
    fault_total_data = Common.T_AHU_SENSING_INFO(EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo)

    fault_total_data['DATE'] = pd.to_datetime(fault_total_data['SensingTime'].dt.strftime('%Y%m%d'))
    #fault_data = fault_total_data.query("DATE ==" + OperatingDate)
    startdate = Common.start_date(SiteCode)
    StartMonth, EndMonth = Common.T_OPERATING_CONFIG(SiteCode)

    """
    if (OperatingDate < startdate):
        print("유효한 날짜의 데이타가 아닙니다!")
        return
    """

    if(AirCondition=="1"):
        fault_data = fault_total_data.query("DATE ==" + OperatingDate)
        """
        if (startdate[4:6] >= str(StartMonth) and startdate[4:6] <= str(EndMonth)):
            fault_data = fault_total_data.query("DATE ==" + OperatingDate)
        else:
            print("유효한 날짜의 데이타가 아닙니다!")
            return
        """

    if(AirCondition=="2"):
        fault_data = fault_total_data.query("DATE ==" + OperatingDate)
        """
        if(int(OperatingDate[4:6]) < StartMonth):
            if( int(startdate[4:6]) < StartMonth):
                fault_data = fault_total_data.query("DATE ==" + OperatingDate)
                print("fault_total_data.query 실행 StartMonth")
        elif (int(OperatingDate[4:6]) > EndMonth):
            if (int(startdate[4:6]) > EndMonth):
                fault_data = fault_total_data.query("DATE ==" + OperatingDate)
                print("fault_total_data.query 실행 EndMonth")
        else:
            print("유효한 날짜의 데이타가 아닙니다!")
            return
        """

    if(len(fault_data)==0):
        print("지정한 운영일의 데티어가 없습니다.")
        return
    sa_set_temp_c, sa_set_temp_h, sa_flow, oa_flow, ea_flow = Common.ahu_info(EquipmentClassCode, EquipmentNo, SiteCode,
                                                                       BuildingNo, ZoneNo)
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
        # 코일밸브 평균 및 표준편차
        coilvlv_mean = round(fault_data['CoolCVlv'].mean(), 2)
        coilvlv_std = round(fault_data['CoolCVlv'].std(), 2)
    if (AirCondition == "2"):
        # 코일밸브 평균 및 표준편차
        coilvlv_mean = round(fault_data['HeatCVlv'].mean(), 2)
        coilvlv_std = round(fault_data['HeatCVlv'].std(), 2)

    # 외기댐퍼개도율(OA-DAMPER) 평균 및 표준편차
    oadamper_mean = round(fault_data['OADamper'].mean(), 2)
    oadamper_std = round(fault_data['OADamper'].std(), 2)

    # 환기댐퍼개도율(OA-DAMPER) 평균 및 표준편차
    radamper_mean = round(fault_data['RADamper'].mean(), 2)
    radamper_std = round(fault_data['RADamper'].std(), 2)

    # 배기댐퍼개도율(OA-DAMPER) 평균 및 표준편차
    eadamper_mean = round(fault_data['EADamper'].mean(), 2)
    eadamper_std = round(fault_data['EADamper'].std(), 2)

    if (AirCondition == "1"):
        columns_customed = ['OATemp', 'SATemp', 'MATemp', 'RATemp', 'CoolCVlv', 'SAFlow', 'OAFlow', 'OADamper', 'SFPower']
    if (AirCondition == "2"):
        columns_customed = ['OATemp', 'SATemp', 'MATemp', 'RATemp', 'HeatCVlv', 'SAFlow', 'OAFlow', 'OADamper', 'SFPower']
    fault_predict = fault_data[columns_customed]

    print('실행 날짜:', OperatingDate)
    print('fault_predict 길이:', len(fault_predict))
    print('fault_predict.size:', fault_predict.size)
    print('fault_predict.shape:', fault_predict.shape)

    ### 새로 수정 추가한 부분 start
    ### 매번 다항회귀 모델에 적용하여 보정 전력값을 산출
    F_fanpower = fault_predict['SFPower'].values

    # 공조기 유사도 기준 정보에서 degree 값 읽어서 사용
    cv_rmse, wss_dstnc, enrgy_dstnc, polydegree = Common.T_AHU_CRITERIA_SIMILARITY_INFO(EquipmentClassCode, EquipmentNo,
                                                                                 SiteCode, BuildingNo, ZoneNo,
                                                                                 CoolHeatingIndication)
    print("poly_degree :", cv_rmse, wss_dstnc, enrgy_dstnc, polydegree)

    poly_features = PolynomialFeatures(degree=polydegree, include_bias=False)
    F_fanpower = poly_features.fit_transform(F_fanpower.reshape(-1, 1))

    if (AirCondition == '1'):
        poly_reg = joblib.load("./STD-cooling-polynomial.pkl")

    if (AirCondition == '2'):
        poly_reg = joblib.load("./STD-heating-polynomial.pkl")

    fanpower_adj = poly_reg.predict(F_fanpower)

    del fault_predict['SFPower']

    fault_predict['SFPower'] = fanpower_adj

    ### 새로 수정하는 부분 end

    # 예측값과 실제 값의 비교
    dataset = fault_predict.values
    X_check = dataset[:, 0:-1]
    Y_check = dataset[:, -1]
    predict_len = Y_check.size

    if (AirCondition == '1'):
        bfaultRFModel = joblib.load("./AHU-cooling-regression.pkl")
    if (AirCondition == '2'):
        bfaultRFModel = joblib.load("./AHU-heating-regression.pkl")

    # (10) 고장진단용 추정 급기팬 전력량 (SAFpower6) : Y_prediction3
    Y_predict_check = bfaultRFModel.predict(X_check).flatten()

    mbe = (np.sum(Y_predict_check) - np.sum(Y_check)) / predict_len
    mae = mean_absolute_error(Y_predict_check, Y_check)
    mse = mean_squared_error(Y_predict_check, Y_check)
    rmse = np.sqrt(mse)
    mean = np.mean(Y_check)
    cvmbe = mbe / mean
    cvmae = mae / mean
    cvrmse = rmse / mean

    fanpower_capacity = 1

    # R2
    r2 = r2_score(Y_check, Y_predict_check)
    # Wasserstein 거리
    wsd = wasserstein_distance(Y_check * fanpower_capacity, Y_predict_check * fanpower_capacity)
    # Energy거리
    cramerd = energy_distance(Y_check * fanpower_capacity, Y_predict_check * fanpower_capacity)

    s_cvrmse = round(cvrmse * 100, 3)
    s_wsd = round((wsd / mean) * 100, 4)
    s_cramerd = round((cramerd / mean) * 100, 4)
    err_no = 0

    if (cv_rmse < cvrmse * 100):
        err_no = err_no + 1
    if (wss_dstnc < (wsd / mean) * 100):
        err_no = err_no + 1
    if (enrgy_dstnc < (cramerd / mean) * 100):
        err_no = err_no + 1

    print('err_no :', err_no)

    # 출력
    print('ASHRAE 데이터 날짜  ; ' + OperatingDate)
    print('시험 Cv(RMSE) % ;   ' + str(s_cvrmse))
    print('와서스타인변동계수%;' + str(s_wsd))
    print('에너지변동계수 %;   ' + str(s_cramerd))

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
    print('코일밸브 평균;      ' + str(coilvlv_mean))
    print('코일밸브 표준편차;  ' + str(coilvlv_std))
    print('외기댐퍼개도율 평균;     ' + str(oadamper_mean))
    print('외기댐퍼개도율 표준편차; ' + str(oadamper_std))
    print('환기댐퍼개도율 평균;     ' + str(radamper_mean))
    print('환기댐퍼개도율 표준편차; ' + str(radamper_std))
    print('배기댐퍼개도율 평균;     ' + str(eadamper_mean))
    print('배기댐퍼개도율 표준편차; ' + str(eadamper_std))

    plot.figure(figsize=(12, 5))
    plot.plot(np.arange(predict_len), Y_predict_check, 'r', label="정상 추정 급기팬 전력량")
    plot.plot(np.arange(predict_len), Y_check, 'b', label="실측 보정 급기팬 전력량")
    plot.legend()
    plot.title("고장")
    plot.show()

    db = Common.conn()
    cursor = db.cursor()
    for i in range(predict_len):
        label = round(Y_check[i], 3)
        prediction = round(Y_predict_check[i], 3)
        row_num = i + 1
        # if (i%17 == 0):
        print("순서 {:d}  보정 {:.8f}  추정 {:.8f}  날짜 {:s}".format(i, label, prediction, OperatingDate))
        ### AHU 센싱정보 테이블 수정
        ### T_AHU_SENSING_INFO Update start
        sql = "UPDATE T_AHU_SENSING_INFO           \
                   SET CorrectionSFPower = %d      \
                      ,PredictionSFPower = %d      \
                  FROM T_AHU_SENSING_INFO a        \
                       JOIN ( SELECT ROW_NUMBER() OVER (ORDER BY sensingtime) AS rownum, sensingtime \
                                  FROM T_AHU_SENSING_INFO        \
                                  WHERE EquipmentClassCode = %s  \
                                  AND   EquipmentNo = %d         \
                                  AND   SiteCode = %s            \
                                  AND   BuildingNo = %s          \
                                  AND   ZoneNo = %d              \
                                  AND format(CAST(sensingtime AS date), 'yyyyMMdd') = %s ) b \
                            ON a.sensingtime = b.sensingtime           \
                 WHERE b.rownum = %d                "
        val = (label, prediction, EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, OperatingDate, row_num)
        cursor.execute(sql, val)
        # print("prediction, label, OperatingDate, row_num")
        ### T_AHU_SENSING_INFO Update end
        """
        """
    print("T_AHU_SENSING_INFO 테이블에서 ", row_num, "개의 레코드가 수정되었습니다.")

    # for i in range(predict_len):
    #    label = Y_pred2[i]
    #    print("{:.8f}".format(label))

    if (err_no <= 1):
        print(" 유사도 비교 결과 \"정상\" 상태입니다.")
        print('---------------------------------------')

        ### 공조기 유사도 실측 테이블 입력
        ### T_AHU_REAL_SIMILARITY_INFO start
        fault_yn = 'N'
        fault_type = 0
        diagnosis_order = '0'

        if (AirCondition == '1'):
            CoolHeatInd = '1'
        if (AirCondition == '2'):
            CoolHeatInd = '2'

        dt_now = dt.datetime.now()
        ddate = OperatingDate
        sdate = dt_now.strftime("%Y%m%d %H:%M:%S")
        print("sdate:", ddate, sdate)

        sql = "INSERT INTO T_AHU_REAL_SIMILARITY_INFO (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, DiagnosisDate, CoolHeatingIndication, CvRMSE, WassersteinDistance, EnergyDistance, FaultYN, FaultType, DiagnosisOrder, SaveTime) VALUES (%s, %d, %s, %s, %d, %s, %s, %d, %d, %d, %s, %d, %s, %s)"
        val = (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, ddate, CoolHeatInd, s_cvrmse, s_wsd, s_cramerd, fault_yn, diagnosis_order, fault_type, sdate)

        cursor.execute(sql, val)
        ### T_AHU_REAL_SIMILARITY_INFO end

    else:
        if (coilvlv_std < 0.03) and (AirCondition == '1'):
            if (coilvlv_mean != 0) and (coilvlv_mean != 1) and (coilvlv_mean != 0.6) and (coilvlv_mean != 0.3) :
                print("냉방코일 밸브 고착(부분 열림 -", int(coilvlv_mean*100), "%)")   # 고장번호 22
                return
            if (coilvlv_std < 0.03) and (AirCondition == '2'):
                if (coilvlv_mean != 0) and (coilvlv_mean != 1) and (coilvlv_mean != 0.6) and (coilvlv_mean != 0.3):
                    print("난방코일 밸브 고착(부분 열림 -", int(coilvlv_mean * 100), "%)")  # 고장번호 23
                    return
            if oadamper_std < 0.03:
                if (oadamper_mean != 0) and (oadamper_mean != 1) and (oadamper_mean != 0.6) and (oadamper_mean != 0.3):
                    print("외기댐퍼 고착(부분 열림 -", int(oadamper_mean * 100), "%)")  # 고장번호 24
                    return
            if radamper_std < 0.03:
                if radamper_mean == 0:
                    print("환기댐퍼 고착(완전 닫힘)")  # 고장번호 25
                else:
                    if radamper_mean == 1:
                        print("환기댐퍼 고착(완전 열림)")  # 고장번호 27
                    else:
                        print("환기댐퍼 고착(부분 열림 -", int(radamper_mean * 100), "%)")  # 고장번호 26
                return

            if eadamper_std < 0.03:
                if eadamper_mean == 0:
                    print("배기댐퍼 고착(완전 닫힘)")  # 고장번호 28
                else:
                    if eadamper_mean == 1:
                        print("배기댐퍼 고착(완전 열림)")  # 고장번호 30
                    else:
                        print("배기댐퍼 고착(부분 열림 -", int(eadamper_mean * 100), "%)")  # 고장번호 29
                return

        print("1차 고장 진단을 실행합니다.")
        print('---------------------------------------')

        ###########################################
        ########### 1차 고장진단 실행 #############
        ###########################################

        df_len = 720 * 0
        fault_count = 90000

        err_cl_acc = {}
        for eno in np.arange(1, 22):

            if (AirCondition == "1" and (16 >= eno >= 13)):
                continue

            if (AirCondition == "2" and ((eno == 3) | (12 >= eno >= 9) | (eno >= 18))):
                continue

            fault_data = fault_total_data.query("DATE ==" + OperatingDate)
            # fault_data = fault_total_data.query('DATE == @OperatingDate')

            sa_set_temp_c, sa_set_temp_h, sa_flow, oa_flow, ea_flow = Common.ahu_info(EquipmentClassCode, EquipmentNo,
                                                                               SiteCode, BuildingNo, ZoneNo)

            if (AirCondition == "1"):
                sa_set_temp = sa_set_temp_c
            else:
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

            df_predict = fault_data

            df_predict['FaultType'] = 1
            # df_predict['SFPower'] = fanpower_adj
            df_predict['SFPower'] = fault_predict['SFPower']

            if (AirCondition == "1"):
                if eno != 10:
                    columns_customed = ['OATemp', 'SATemp', 'MATemp', 'RATemp', 'CoolCVlv', 'SAFlow', 'OAFlow',
                                        'OADamper', 'SFPower', 'FaultType']
                else:
                    columns_customed = ['OATemp', 'MATemp', 'RATemp', 'CoolCVlv', 'SAFlow', 'OAFlow', 'OADamper',
                                        'SFPower', 'FaultType']

            if (AirCondition == "2"):
                if eno != 10:
                    columns_customed = ['OATemp', 'SATemp', 'MATemp', 'RATemp', 'HeatCVlv', 'SAFlow', 'OAFlow',
                                        'OADamper', 'SFPower', 'FaultType']
                else:
                    columns_customed = ['OATemp', 'MATemp', 'RATemp', 'HeatCVlv', 'SAFlow', 'OAFlow', 'OADamper',
                                        'SFPower', 'FaultType']

            df_predict = df_predict[columns_customed]
            #print("df_predict:",df_predict)

            # 예측값과 실제 값의 비교
            dataset = df_predict.values
            X_real = dataset[:, 0:-1]
            Y_real = dataset[:, -1]

            test_len = len(Y_real)

            if (AirCondition == '1'):
                path = "./STD-cooling-fault-%02d.pkl" % eno

            if (AirCondition == '2'):
                path = "./STD-heating-fault-%02d.pkl" % eno

            print('path:', path)

            classRFModel = joblib.load(path)

            Y_pred = classRFModel.predict(X_real).flatten()
            Y_pred_list = Y_pred.tolist()

            max_count = 0
            for i in range(fault_count):
                acc_count = Y_pred_list.count(i)
                if Y_pred_list.count(i) > 0:
                    print("Y_pred_list.count(%d):" % i, Y_pred_list.count(i))
                if acc_count > max_count:
                    max_count = acc_count
                    acc_fault = i
                    print("acc_fault(%d):" % i, acc_fault)

            print('test_len:', test_len)
            print('acc_count:', acc_count)
            print('max_count:', max_count)
            print('acc_fault:', acc_fault)

            print("")
            print("정확도 갯수: {:d}".format(max_count))
            print("정확도     : {:.2f}%".format(max_count / test_len * 100))
            print("고장   유형: {:02d}".format(acc_fault))

            # generate confusion matrix
            pList = Y_pred.tolist()
            confusionMat = confusion_matrix(Y_real, pList)

            print('')
            print("Confusion Matrix")
            print(confusionMat)
            print('')

            true_count = 0

            for i in range(test_len):
                label = Y_real[i]
                pred = Y_pred[i]
                # if ((label != 1 or pred != 0) or (label != 0 and pred != 0)) :
                #print("실측 고장: %d"%label, "예측 고장: %d"%pred)

                if label == pred:
                    true_count = true_count + 1

            print('true_count:', true_count)
            accuracy = accuracy_score(Y_real, Y_pred)
            if (accuracy * 100 >= 80):
                # err_acc.append(accuracy*100)
                key = eno
                val = round(accuracy * 100, 2)
                err_cl_acc[key] = val

            print("예측 고장수: {:.0f}".format(true_count))
            print("실측 고장수: {:.0f}".format(test_len))
            print("예측 정확도: {:.2f}%".format(accuracy * 100))
            print('---------------------------------------')

            if (accuracy > 0):
                #########################################
                ### 공조기 고장 진단 정보 테이블 입력
                ### T_AHU_FAULT_DIAGNOSIS_INFO start
                diagnosis_order = '1'
                fault_type = str(eno)
                class_accuracy = round(accuracy * 100, 2)

                if (AirCondition == '1'):
                    CoolHeatInd = '1'
                if (AirCondition == '2'):
                    CoolHeatInd = '2'

                dt_now = dt.datetime.now()
                ddate = OperatingDate
                sdate = dt_now.strftime("%Y%m%d %H:%M:%S")
                #print("sdate:", ddate, sdate)

                sql = "INSERT INTO T_AHU_FAULT_DIAGNOSIS_INFO (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, DiagnosisOrder, DiagnosisDate, FaultType, ClassificationAccuracy, SaveTime) VALUES (%s, %d, %s, %s, %d, %s, %s, %d, %d, %s)"
                val = (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, diagnosis_order, ddate, fault_type, class_accuracy, sdate)

                cursor.execute(sql, val)
                ### T_AHU_FAULT_DIAGNOSIS_INFO end
                #########################################

        err_count = len(err_cl_acc.keys())
        if (err_count == 0):
            print("1차 진단 결과 \"정상 상태\" 입니다.")
            print('---------------------------------------')

            ### 공조기 유사도 실측 테이블 입력
            ### T_AHU_REAL_SIMILARITY_INFO start
            fault_yn = 'Y'
            fault_type = 0
            diagnosis_order = '1'

            if (AirCondition == '1'):
                CoolHeatInd = '1'
            if (AirCondition == '2'):
                CoolHeatInd = '2'

            dt_now = dt.datetime.now()
            ddate = OperatingDate
            sdate = dt_now.strftime("%Y%m%d %H:%M:%S")
            class_accuracy = 100
            print("sdate:", ddate, sdate)

            sql = "INSERT INTO T_AHU_REAL_SIMILARITY_INFO (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, DiagnosisDate, CoolHeatingIndication, CvRMSE, WassersteinDistance, EnergyDistance, FaultYN, DiagnosisOrder, FaultType, ClassificationAccuracy, SaveTime) VALUES (%s, %d, %s, %s, %d, %s, %s, %d, %d, %d, %s, %s, %d, %d, %s)"
            val = (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, ddate, CoolHeatInd, s_cvrmse, s_wsd,
                   s_cramerd, fault_yn, diagnosis_order, fault_type, class_accuracy, sdate)

            cursor.execute(sql, val)
            ### T_AHU_REAL_SIMILARITY_INFO end

        else:
            print("2차 고장 진단을 실행합니다.")
            print('---------------------------------------')
            #print("분류정확도 : ", err_cl_acc.items())

            ######################################################################
            ########### 표준 공조기 2차 고장 유형 분류 모델 생성 #################
            ######################################################################

            # fault_total = pd.read_csv(criteria_file_path + criteria_file_name, header = 0, delimiter = ',', quoting = 3)
            fault_total = Common.T_STD_SENSING_INFO(AirCondition)

            fault_kind = {}
            err_num = 0
            #err_key_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            err_key_list = [0 for i in range(10)]

            for i in range(22):
                key = i
                value = err_cl_acc.get(i)
                if (value != None):
                    err_num = err_num + 1
                    fault_kind[key] = value
                    print('고장번호:{:2d}, 분류 정확도(%):{:.2f}'.format(i, value))

            key_list = list(fault_kind.keys())
            #print("key_list : ", key_list)
            #print("len(key_list) : ", len(key_list))
            #print("분류 고장번호 : ", fault_kind.items())
            print("분류 고장번호 개수 : ", err_num)

            for i in range(err_num):
                err_key_list[i] = key_list[i]
                #print("err_key_list[{:d}]={:d}".format(i, err_key_list[i]))

            if (err_num == 0):
                print("1차 진단 결과 \"정상 상태\"입니다.")
                db.commit()
                cursor.close()
                db.close()
                return (None, err_num, err_key_list)

            # class_accuracy = round(val,2)
            if (err_num == 1):
                print("2차 진단 결과 \"고장 상태\"입니다.")
                print('고장 번호는 {:2d} 입니다'.format(key_list[0]))
                print("--------------------------------------------------")

                ### 공조기 유사도 실측 테이블 입력
                ### T_AHU_REAL_SIMILARITY_INFO start
                fault_yn = 'Y'
                fault_type = key_list[0]
                diagnosis_order = '2'
                values = fault_kind[fault_type]

                if (AirCondition == '1'):
                    CoolHeatInd = '1'
                if (AirCondition == '2'):
                    CoolHeatInd = '2'

                dt_now = dt.datetime.now()
                ddate = OperatingDate
                sdate = dt_now.strftime("%Y%m%d %H:%M:%S")
                # value = 100.0

                sql = "INSERT INTO T_AHU_REAL_SIMILARITY_INFO (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, DiagnosisDate, CoolHeatingIndication, CvRMSE, WassersteinDistance, EnergyDistance, FaultYN, DiagnosisOrder, FaultType, ClassificationAccuracy, SaveTime) VALUES (%s, %d, %s, %s, %d, %s, %s, %d, %d, %d, %s, %s, %d, %d, %s)"
                val = (
                EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, ddate, CoolHeatInd, s_cvrmse, s_wsd,
                s_cramerd, fault_yn, diagnosis_order, fault_type, values, sdate)
                cursor.execute(sql, val)

                sql = "INSERT INTO T_AHU_FAULT_DIAGNOSIS_INFO (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, DiagnosisOrder, DiagnosisDate, FaultType, ClassificationAccuracy, SaveTime) VALUES (%s, %d, %s, %s, %d, %s, %s, %d, %d, %s)"
                val = (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, diagnosis_order, ddate, fault_type, values, sdate)
                cursor.execute(sql, val)

                db.commit()
                cursor.close()
                db.close()
                ### T_AHU_REAL_SIMILARITY_INFO end
                return (None, err_num, err_key_list)

            for i in range(1, 11 - err_num):
                err_key_list[10 - i] = key_list[err_num - 1]
                #print("key_list[{:d}]={:d} ".format(10 - i, key_list[err_num - 1]))
                #print("err_key_list[{:d}]={:d}".format(10 - i, err_key_list[10 - i]))

            fault_total = fault_total[(fault_total['FaultType'] == err_key_list[0]) |
                                      (fault_total['FaultType'] == err_key_list[1]) |
                                      (fault_total['FaultType'] == err_key_list[2]) |
                                      (fault_total['FaultType'] == err_key_list[3]) |
                                      (fault_total['FaultType'] == err_key_list[4]) |
                                      (fault_total['FaultType'] == err_key_list[5]) |
                                      (fault_total['FaultType'] == err_key_list[6]) |
                                      (fault_total['FaultType'] == err_key_list[7]) |
                                      (fault_total['FaultType'] == err_key_list[8]) |
                                      (fault_total['FaultType'] == err_key_list[9])]

            fault10 = 0
            for i in range(err_num):
                fault_total['FaultType'] = fault_total['FaultType'].replace(err_key_list[i], i)
                if (err_key_list[i] == 10):
                    fault10 = 1
            #print("fault10 :", fault10, AirCondition)

            if (fault10 == 1):
                # 결함 10번인 경우 SUPPLY-TEMP 제외
                columns_customed = ['OATemp', 'MATemp', 'RATemp', 'CoilVlv', 'SAFlow', 'OAFlow', 'OADamper', 'SFPower',
                                    'FaultType']
            else:
                columns_customed = ['OATemp', 'SATemp', 'MATemp', 'RATemp', 'CoilVlv', 'SAFlow', 'OAFlow', 'OADamper',
                                    'SFPower', 'FaultType']

            fault_total = fault_total[columns_customed]

            fault_type = fault_total['FaultType'].unique()
            #print('fault_type:', fault_type)

            faultNames = np.array(fault_total.keys())
            #print('faultNames:', faultNames)

            dataset = fault_total.values
            X = dataset[:, 0:-1]
            Y = dataset[:, -1]

            xTrain, xTest, yTrain, yTest = train_test_split(X, Y, test_size=0.30, stratify=Y, random_state=531)

            iTrees = 500
            depth = None
            maxFeat = 2  # try tweaking
            classRFModel = ensemble.RandomForestClassifier(n_estimators=iTrees, max_depth=depth, max_features=maxFeat,
                                                           oob_score=False, random_state=531, n_jobs=-1)

            classRFModel.fit(xTrain, yTrain)

            # Accumulate auc on test set
            prediction = classRFModel.predict(xTest)
            prediction_len = prediction.size
            print('prediction_len:', prediction_len)
            print('prediction:', prediction)

            correct = accuracy_score(yTest, prediction)
            precision = precision_score(yTest, prediction, average='macro')
            recall = recall_score(yTest, prediction, average='macro')

            print("정확도 : ", correct)
            print("정밀도 : ", precision)
            print("재현율 : ", recall)
            print("F1비율 : ", 2 * precision * recall / (precision + recall))

            # generate confusion matrix
            pList = prediction.tolist()
            confusionMat = confusion_matrix(yTest, pList)
            # confusionMat = confusion_matrix(yyTest, pList)

            print('')
            print("Confusion Matrix")
            print(confusionMat)
            print('')

            rowcount = confusionMat.shape[0]
            colcount = confusionMat.shape[1]
            #print('rowcount:', rowcount)
            #print('colcount:', colcount)

            for i in range(rowcount):
                fault_count = 0
                for j in range(colcount):
                    fault_count = fault_count + confusionMat[i, j]
                fault_accuracy = confusionMat[i, i] / fault_count * 100
                print("고장 {:02d}  정확도: {:.2f}".format(fault_type[i], fault_accuracy))
                # print("순서 {:d} confusionMat[i,i] {:d}  fault_count: {:d}". format(i, confusionMat[i,i], fault_count))

            # Plot feature importance
            featureImportance = classRFModel.feature_importances_

            # normalize by max importance
            featureImportance = featureImportance / featureImportance.max()

            # plot variable importance
            idxSorted = np.argsort(featureImportance)
            barPos = np.arange(idxSorted.shape[0]) + .5
            plot.barh(barPos, featureImportance[idxSorted], align='center')
            plot.yticks(barPos, faultNames[idxSorted])
            plot.xlabel('특성 중요도', fontproperties=fontprop)
            plot.show()

            #######################################################
            ########### 운용 공조기 2차 고장 진단 #################
            #######################################################

            if (fault10 == 1):
                del df_predict['SATemp']

            dataset_pred = df_predict.values
            X_pred = dataset_pred[:, 0:-1]
            Y_real = dataset_pred[:, -1]

            test_len = len(Y_real)

            # 표준 고장 데이터 진단한 모델로 운용공조기 고장 데이터 예측
            ######################################################
            Y_pred = classRFModel.predict(X_pred).flatten()
            #print("Y_pred size : ", Y_pred.size)
            #print("err_key_list : ", err_key_list)

            Y_pred_list = Y_pred.tolist()

            max_count = 0
            for i in range(10):
                acc_count = Y_pred_list.count(i)
                if acc_count != 0:
                    print('Y_pred_list.count({:d}) : {:d}'.format(i, Y_pred_list.count(i)))
                if acc_count > max_count:
                    max_count = acc_count
                    acc_fault = i
                    print('max_count:', i, max_count)

            acc_fault = err_key_list[acc_fault]

            print("")
            print("정확도 갯수: {:d}".format(max_count))
            print("정확도    : {:.2f}%".format(max_count / test_len * 100))
            print("고장   유형: {:02d}".format(acc_fault))

            # generate confusion matrix
            confusionMat = confusion_matrix(Y_real, Y_pred_list)

            print('')
            print("Confusion Matrix")
            print(confusionMat)
            print('')

            true_count = 0

            for i in range(test_len):
                label = Y_real[i]
                pred = Y_pred[i]
                #print("실측 고장: %d"%label, "예측 고장: %d"%pred)
                if label == pred:
                    true_count = true_count + 1
                    #if (label != 0):
                    #print("실측 고장: %d"%label, "예측 고장: %d"%pred)

            accuracy = accuracy_score(Y_real, Y_pred)

            print("예측 고장수: {:.0f}".format(true_count))
            print("실측 고장수: {:.0f}".format(test_len))
            print("예측 정확도: {:.2f}%".format(accuracy * 100))
            print("--------------------------------------------------")
            print("2차 고장 진단 결과 고장 유형 :{:02d}, 정확도 : {:.2f}% 입니다.".format(acc_fault, max_count / test_len * 100))
            print("=======================================================")

            class_accuracy = round(max_count / test_len * 100, 2)
            if (class_accuracy > 0):
                #########################################
                ### 공조기 고장 진단 정보 테이블 입력
                ### T_AHU_FAULT_DIAGNOSIS_INFO start
                diagnosis_order = '2'
                fault_type = acc_fault

                if (AirCondition == '1'):
                    CoolHeatInd = '1'
                if (AirCondition == '2'):
                    CoolHeatInd = '2'

                dt_now = dt.datetime.now()
                ddate = OperatingDate
                sdate = dt_now.strftime("%Y%m%d %H:%M:%S")
                #print("sdate:", ddate, sdate)

                sql = "INSERT INTO T_AHU_FAULT_DIAGNOSIS_INFO (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, DiagnosisOrder, DiagnosisDate, FaultType, ClassificationAccuracy, SaveTime) VALUES (%s, %d, %s, %s, %d, %s, %s, %d, %d, %s)"
                val = (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, diagnosis_order, ddate, fault_type, class_accuracy, sdate)

                cursor.execute(sql, val)
                ### T_AHU_FAULT_DIAGNOSIS_INFO end
                #########################################

            ### 공조기 유사도 실측 테이블 입력
            ### T_AHU_REAL_SIMILARITY_INFO start
            fault_yn = 'Y'
            fault_type = acc_fault
            diagnosis_order = '2'

            if (AirCondition == '1'):
                CoolHeatInd = '1'
            if (AirCondition == '2'):
                CoolHeatInd = '2'

            dt_now = dt.datetime.now()
            ddate = OperatingDate
            sdate = dt_now.strftime("%Y%m%d %H:%M:%S")
            #print("sdate:", ddate, sdate)

            sql = "INSERT INTO T_AHU_REAL_SIMILARITY_INFO (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, DiagnosisDate, CoolHeatingIndication, CvRMSE, WassersteinDistance, EnergyDistance, FaultYN, DiagnosisOrder, FaultType, ClassificationAccuracy, SaveTime) VALUES (%s, %d, %s, %s, %d, %s, %s, %d, %d, %d, %s, %s, %d, %d, %s)"
            val = (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, ddate, CoolHeatInd, s_cvrmse, s_wsd,
                   s_cramerd, fault_yn, diagnosis_order, fault_type, class_accuracy, sdate)

            cursor.execute(sql, val)
            #print(cursor.rowcount, "개의 레코드가 입력되었습니다.")
            ### T_AHU_REAL_SIMILARITY_INFO end

    db.commit()
    cursor.close()
    db.close()
