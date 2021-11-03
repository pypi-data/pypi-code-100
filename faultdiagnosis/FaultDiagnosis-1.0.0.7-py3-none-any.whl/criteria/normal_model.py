# normal_model.py

from Criteria.common_functions import *

from matplotlib import font_manager, rc
rc('font', family=font_manager.FontProperties(fname="\c:/Windows/Fonts/malgun.ttf").get_name())
fontprop = font_manager.FontProperties(fname="\c:/Windows/Fonts/malgunbd.ttf", size=12)

from sklearn.model_selection import train_test_split
from sklearn import ensemble
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, precision_score, recall_score, confusion_matrix
from scipy.stats import wasserstein_distance
from scipy.stats import energy_distance
import matplotlib.pylab as plot
import numpy as np
import pandas as pd
import joblib
import pymssql
import warnings
warnings.filterwarnings('ignore')

class CriteriaModel:
    SiteCode = ""

    def __init__(self, Sitecode):
        self.SiteCode = Sitecode
        CriteriaModel.SiteCode = Sitecode

    def standard_model(self):
        SiteCode = Common.sitecode(Common.SiteCode)
        if (len(SiteCode) != 8 or len(SiteCode) < 8 or SiteCode == ''):
            print('사이트코드가 존재하지 않습니다.')
            sys.exit(0)

        AirCondition = Common.air_condition(SiteCode)
        if (len(AirCondition) != 1 or len(AirCondition) < 1 or AirCondition == ''):
            print('냉난방구분값이 존재하지 않습니다.')
            sys.exit(0)

        df_fault = Common.T_STD_SENSING_INFO(AirCondition)
        if ((AirCondition == '1' and len(df_fault) < 152262) or (AirCondition == '2' and len(df_fault) < 120076)):
            print('정상적인 표준 센싱 정보 데이터가 존재하지 않습니다.')
            sys.exit(0)

        df_fault = df_fault[(df_fault['FaultType'] == 0)]
        columns_customed = ['OATemp', 'SATemp', 'RATemp', 'MATemp', 'CoilVlv', 'SAFlow', 'OAFlow', 'OADamper', 'SFPower']
        df_fault = df_fault[columns_customed]

        faultNames = np.array(df_fault.keys())
        dataset = df_fault.values
        X = dataset[:,0:-1]
        Y = dataset[:,-1]

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

        #train random forest at a range of ensemble sizes in order to see how the mse changes
        iTrees = 500
        depth = None
        maxFeat  = 2 #try tweaking
        afaultRFModel = ensemble.RandomForestRegressor(n_estimators=iTrees, max_depth=depth, max_features=maxFeat,
                                                       oob_score=False, random_state=42, n_jobs=-1)

        afaultRFModel.fit(X_train,Y_train)

        # 모델 저장하기
        # (1) 표준 공조기 정상 유형 회귀모델
        #aircondition = air_condition('GGTMC042')
        if(AirCondition == "1"):
            joblib.dump(afaultRFModel, "./STD-cooling-regression.pkl")
        if(AirCondition == "2"):
            joblib.dump(afaultRFModel, "./STD-heating-regression.pkl")

        #Accumulate mse on test set
        train_score = afaultRFModel.score(X_train, Y_train)
        Y_prediction_train = afaultRFModel.predict(X_train)
        Y_prediction = afaultRFModel.predict(X_test)

        test_len = Y_test.size
        mean = np.mean(Y_test)
        mbe = (np.sum(Y_prediction) - np.sum(Y_test)) / test_len
        mae = mean_absolute_error(Y_prediction, Y_test)
        mse = mean_squared_error(Y_prediction, Y_test)
        rmse = np.sqrt(mse)
        cvmbe = mbe / mean
        cvmae = mae / mean
        cvrmse = rmse / mean

        # R2
        r2_train = r2_score(Y_train, Y_prediction_train)
        r2_test = r2_score(Y_test, Y_prediction)

        # Wasserstein 거리
        wsd = wasserstein_distance(Y_test, Y_prediction)

        # Energy거리
        cramerd = energy_distance(Y_test, Y_prediction)

        # 출력
        print('시험 Cv(RMSE) % ; ' + str(cvrmse * 100))
        print('와서스타인변동계수;' + str(wsd/mean*100))
        print('에너지거리변동계수;' + str(cramerd/mean*100)+'\n')
        print('실측 평균(시험) : ' + str(mean))
        print('시험 MBE :        ' + str(mbe))
        print('시험 MAE :        ' + str(mae))
        print('시험 MSE :        ' + str(mse))
        print('시험 RMSE :       ' + str(rmse))
        print('훈련 R2 % ;       ' + str(r2_train * 100))
        print('시험 R2 % ;       ' + str(r2_test * 100))
        print('시험 Cv(MBE) % ;  ' + str(cvmbe * 100))
        print('시험 Cv(MAE) % ;  ' + str(cvmae * 100))
        print('와서스테인거리;   ' + str(wsd))
        print('에너지거리;        ' + str(cramerd))

        # normalize by max importance
        featureImportance = afaultRFModel.feature_importances_
        featureImportance = featureImportance / featureImportance.max()

        sorted_idx = np.argsort(featureImportance)
        barPos = np.arange(sorted_idx.shape[0]) + .5

        plot.barh(barPos, featureImportance[sorted_idx], align='center')
        plot.yticks(barPos, faultNames[sorted_idx])
        plot.xlabel('특성 중요도', fontproperties=fontprop)
        plot.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
        plot.show()

        plot.figure(figsize=(12,5))
        plot.plot(Y_test, 'b--', label="실측 급기팬 전력량")
        plot.plot(Y_prediction,'y',label="예측 급기팬 전력량")
        plot.legend()
        plot.show()

        for i in range(test_len):
            label = Y_test[i]
            prediction = Y_prediction[i]
            print("{: 5d}    실측:  {:.3f},    예측: {:.3f}".format(i, label, prediction))


    def normal_model(self):
        SiteCode = Common.sitecode(Common.SiteCode)
        if (len(SiteCode) != 8 or len(SiteCode) < 8 or SiteCode == ''):
            print('사이트코드가 존재하지 않습니다.')
            sys.exit(0)

        AirCondition = Common.air_condition(SiteCode)
        if (len(AirCondition) != 1 or len(AirCondition) < 1 or AirCondition == ''):
            print('냉난방구분값이 존재하지 않습니다.')
            sys.exit(0)

        fault_predict = Common.T_STD_SENSING_INFO(AirCondition)
        if ((AirCondition == '1' and len(fault_predict) < 152262) or (AirCondition == '2' and len(fault_predict) < 120076)):
            print('정상적인 표준 센싱 정보 데이터가 존재하지 않습니다.')
            sys.exit(0)
        fault_predict = fault_predict[(fault_predict['FaultType'] == 0)]

        columns_customed = ['OATemp', 'SATemp', 'RATemp', 'MATemp', 'CoilVlv', 'SAFlow', 'OAFlow', 'OADamper', 'SFPower']
        fault_predict = fault_predict[columns_customed]

        # 예측 값과 실제 값의 비교
        dataset = fault_predict.values
        X_pred0 = dataset[:,0:-1]
        Y_pred0 = dataset[:,-1]
        predict_len = Y_pred0.size

        if(AirCondition == "1"):
            afaultRFModel = joblib.load("./STD-cooling-regression.pkl")
        if(AirCondition == "2"):
            afaultRFModel = joblib.load("./STD-heating-regression.pkl")
        Y_prediction1 = afaultRFModel.predict(X_pred0).flatten()

        mbe = (np.sum(Y_prediction1) - np.sum(Y_pred0)) / predict_len
        mae = mean_absolute_error(Y_prediction1, Y_pred0)
        mse = mean_squared_error(Y_prediction1, Y_pred0)
        rmse = np.sqrt(mse)
        mean = np.mean(Y_pred0)
        cvmbe = mbe / mean
        cvmae = mae / mean
        cvrmse = rmse / mean

        # R2
        r2 = r2_score(Y_pred0, Y_prediction1)
        # Wasserstein 거리
        wsd = wasserstein_distance(Y_pred0, Y_prediction1)
        # Energy거리
        cramerd = energy_distance(Y_pred0, Y_prediction1)

        # 출력
        print('예측 Cv(RMSE) % ; ' + str(cvrmse * 100))
        print('와서스타인변동계수;' + str(wsd/mean*100))
        print('에너지거리변동계수;' + str(cramerd/mean*100)+'\n')

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

        plot.figure(figsize=(12,5))
        plot.plot(np.arange(predict_len),Y_pred0, 'b--', label="실측 급기팬 전력량")
        plot.plot(np.arange(predict_len),Y_prediction1,'c',label="예측 급기팬 전력량")
        plot.legend()
        plot.show()

        for i in range(predict_len):
            label = Y_pred0[i]
            prediction = Y_prediction1[i]
            print("실측:  {:.5f}, 예측: {:.5f}".format(label, prediction))


    def fault_model(self):
        kfault_type1 = 0
        SiteCode = Common.sitecode(Common.SiteCode)
        if (len(SiteCode) != 8 or len(SiteCode) < 8 or SiteCode == ''):
            print('사이트코드가 존재하지 않습니다.')
            sys.exit(0)

        AirCondition = Common.air_condition(SiteCode)
        if (len(AirCondition) != 1 or len(AirCondition) < 1 or AirCondition == ''):
            print('냉난방구분값이 존재하지 않습니다.')
            sys.exit(0)

        for eno in np.arange(1,22):
            if(AirCondition == "1" and ( 16 >= eno >= 13)):
                continue
            if(AirCondition == "2" and ((eno==3) or (12 >= eno >= 9) or (eno >= 18))):
                continue

            #fault_total = pd.read_csv(criteria_file_path + criteria_file_name, header = 0, delimiter = ',', quoting = 3)
            fault_total = Common.T_STD_SENSING_INFO(AirCondition)
            if ((AirCondition == '1' and len(fault_total) < 152262) or (AirCondition == '2' and len(fault_total) < 120076)):
                print('정상적인 표준 센싱 정보 데이터가 존재하지 않습니다.')
                sys.exit(0)

            kfault_type2 = eno
            print('고장번호: ', kfault_type2)
            fault_total = fault_total[(fault_total['FaultType'] == kfault_type1) |
                                      (fault_total['FaultType'] == kfault_type2)]

            fault_total['FaultType'] = fault_total['FaultType'].replace(kfault_type2, 1)

            if kfault_type2 != 10:
                columns_customed = ['OATemp', 'SATemp', 'RATemp', 'MATemp', 'CoilVlv', 'SAFlow', 'OAFlow', 'OADamper', 'SFPower', 'FaultType']
            else :
            #결함 10번인 경우 SUPPLY-TEMP 제외
                columns_customed = ['OATemp', 'RATemp', 'MATemp', 'CoilVlv', 'SAFlow', 'OAFlow', 'OADamper', 'SFPower', 'FaultType']

            fault_total = fault_total[columns_customed]
            fault_type = fault_total['FaultType'].unique()
            print('fault_type:',fault_type)
            faultNames = np.array(fault_total.keys())

            dataset = fault_total.values
            X = dataset[:,0:-1]
            Y = dataset[:,-1]

            xTrain, xTest, yTrain, yTest = train_test_split(X, Y, test_size=0.30, stratify=Y, random_state=531)

            iTrees = 500
            depth = None
            maxFeat  = 2 #try tweaking
            classRFModel = ensemble.RandomForestClassifier(n_estimators=iTrees, max_depth=depth, max_features=maxFeat,
                                                           oob_score=False, random_state=531, n_jobs=-1)
            classRFModel.fit(xTrain,yTrain)

            if(AirCondition == "1"):
                joblib.dump(classRFModel, "./STD-cooling-fault-%02d.pkl" %eno)
            if(AirCondition == "2"):
                joblib.dump(classRFModel, "./STD-heating-fault-%02d.pkl" %eno)

            #Accumulate auc on test set
            prediction = classRFModel.predict(xTest)
            prediction_len = prediction.size
            print('prediction_len:',prediction_len)
            print('prediction:',prediction)

            correct = accuracy_score(yTest, prediction)
            precision = precision_score(yTest, prediction, average='macro')
            recall = recall_score(yTest, prediction, average='macro')

            print("정확도 : ", correct)
            print("정밀도 : ", precision)
            print("재현율 : ", recall)
            print("F1비율 : ", 2 * precision * recall / (precision + recall))

            #generate confusion matrix
            pList = prediction.tolist()

            confusionMat = confusion_matrix(yTest, pList)
            #confusionMat = confusion_matrix(yyTest, pList)

            print('')
            print("Confusion Matrix")
            print(confusionMat)
            print('')

            rowcount = confusionMat.shape[0]
            colcount = confusionMat.shape[1]
            print('rowcount:', rowcount)
            print('colcount:', colcount)

            for i in range(rowcount):
                fault_count = 0
                for j in range(colcount):
                    fault_count = fault_count + confusionMat[i,j]
                fault_accuracy = confusionMat[i,i] / fault_count * 100
                print("고장 {:02d}  정확도: {:.2f}". format(fault_type[i], fault_accuracy))

            # Plot feature importance
            featureImportance = classRFModel.feature_importances_

            # normalize by max importance
            featureImportance = featureImportance / featureImportance.max()

            #plot variable importance
            idxSorted = np.argsort(featureImportance)
            barPos = np.arange(idxSorted.shape[0]) + .5
            plt.barh(barPos, featureImportance[idxSorted], align='center')
            plt.yticks(barPos, faultNames[idxSorted])
            plt.xlabel('특성 중요도', fontproperties=fontprop)
            plt.show()

