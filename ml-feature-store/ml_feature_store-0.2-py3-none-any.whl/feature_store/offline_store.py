#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

import pandas as pd
from typing import Any, Dict, List, Optional, Tuple, Union
import requests
import json
from pyspark.sql import SparkSession
import ml_feature_store.feature_store as feature_store

class FeatureStore:
    feature_query_service_url: str
    spark_session: SparkSession

    def __init__(self, feature_query_service_url: str, spark_session: SparkSession):
        self.feature_query_service_url = feature_query_service_url
        self.spark_session = spark_session

    def get_history_feature_store(self, label_table_path: str, key_name: str, fiele_names: str,
                                  feature_refs: List[str], dts: str, user: str) -> pd.DataFrame:
        # curl "http://localhost:8080/offline_join_features?labelTable=defatic:user_model,magazi011,
        # 20211012&user=80261445&busType=rec"
        submit_job_request = self.feature_query_service_url + '/offline_join_features?' + "labelTable={0}&" \
                                                                                          "lableFieldNames={1}&" \
                                                                                          "uidName={2}&" \
                                                                                          "features={3}&" \
                                                                                          "dss={4}&user={5}".format(
            label_table_path, fiele_names, key_name, ','.join(feature_refs), dts, user)
        print(submit_job_request)
        r = requests.get(submit_job_request)
        task_id = ''
        if r.status_code == 200:
            content = json.loads(r.content)
            task_id = content['task_id']
            print(task_id)
        else:
            raise Exception('submit job failed '+submit_job_request)
        table_name: str
        while 1:
            get_status_request = self.feature_query_service_url + "/get_job_status?" + "taskId=" + task_id
            print(get_status_request)
            r = requests.get(get_status_request)
            if r.status_code == 200:
                content = json.loads(r.content)
                status = content['status']
                app_id = content['appId']
                if status == 'FAILED' or status == 'KILLED':
                    print('spark job failed app id is ' + app_id)
                    raise Exception('job failed app id is ' + app_id)
                    break
                if status == 'FINISHED':
                    table_name = content['tableName']
            else:
                print('http request failed' + app_id)
                break
            time.sleep(30)

        return self.spark_session.sql("select * from " + table_name).toPandas()


if __name__ == '__main__':
    spark_session = SparkSession.builder.config('deploy-mode', 'client').master('local[*]').enableHiveSupport().getOrCreate()
    feature_store = feature_store.offline_store.FeatureStore('http://localhost:8080/', spark_session)
    feature_list = ['magazine.static:user_model', 'magazine.static:user_stage', 'magazine.static:user_province',
                    'magazine.static:user_tourism']
    df = feature_store.get_history_feature_store('default.feeds_label_feature_article_test',
                                                 'userid',
                                                 'predictId,docId,predictscore',
                                                 feature_list, '20211011', '80348083')
    print(df.head())
