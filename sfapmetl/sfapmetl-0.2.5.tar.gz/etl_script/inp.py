import schedule
import time
import ast
import os
import json
import requests
from pushtoES import write_docs_bulk

from datetime import datetime
import datetime as dt
import calendar
from datetime import datetime, timedelta
from dateutil.tz import tzutc, tzlocal
import random
import dateutil.relativedelta
import threading

def iterateDict(data):
    local_dict = {}
    for key,val in data.items():
        if type(val) == unicode:
            local_dict[key.encode("utf-8")] = val.encode("utf-8")
        elif type(val) != dict:
            local_dict.update({key.encode("utf-8"):val})
        elif type(val) == dict:
            local_dict.update({key.encode("utf-8"):iterateDict(val)})
        else:
            local_dict.update({key.encode("utf-8"):val})
    return local_dict

def get_data(urlDict):
    tasksUrl = urlDict.get("url")
    all_data = []
    for url in [tasksUrl]:
        response = requests.get(
            url,
            # params={'duration': '10d'},
            headers={'Authorization': urlDict["authkey"],'Content-type': 'application/json' },
            verify=False
        )
        data = json.loads(response.text)
        # data = ast.literal_eval(json.dumps(data))

        all_data = all_data + data.get("result", [])
    return all_data

def form_task_record(data, flag, tags, curr_time, taskId, bufferData=None):
    metadata = {
         "SCRIPT_NAME": data["SCRIPT_NAME"],
         "TABLE_NAME": data["TABLE_NAME"],
         "LOG_DESC": data["LOG_DESC"],
         "ADDITIONAL_INFO": data["ADDITIONAL_INFO"],
         "IP_ADDRESS": data["IP_ADDRESS"],
         "MODULE_CODE":data["MODULE_CODE"],
         "WORKSTATION": data["WORKSTATION"],
         "HOST_NAME": data["HOST_NAME"]
    }
    rec = {
        "jobName" : data.get("ETL_EXECUTION_ID"),
        "jobId" : data["jobId"],
        "stageName":data["stageName"],
        "time": curr_time,
        "taskName": taskId,
        "status": data['STATUS'],
        "_documentType":"task"
    }
    rec['metaData'] = metadata
    rec.update(tags)
    if flag == 'started':
        rec['startTime'] = data['time']
        rec['started'] = True
    if flag == 'completed':
        if taskId in bufferData.get(data['jobId']).keys():
            record = bufferData.get(data['jobId']).get(taskId)
            rec['duration'] = data['time'] - record['startTime']
            rec['endTime'] = data['time']
            rec['stageName'] = record['stageName']
            rec['startTime'] = record['startTime']
            rec['completed'] = True
        else:
            print("no start record found")
            rec = None
    return rec

def form_job_record(data, flag, tags, curr_time, bufferData=None):
    metadata = {
         "SCRIPT_NAME": data["SCRIPT_NAME"],
         "TABLE_NAME": data["TABLE_NAME"],
         "LOG_DESC": data["LOG_DESC"],
         "ADDITIONAL_INFO": data["ADDITIONAL_INFO"],
         "IP_ADDRESS": data["IP_ADDRESS"],
         "MODULE_CODE":data["MODULE_CODE"],
         "WORKSTATION": data["WORKSTATION"],
         "HOST_NAME": data["HOST_NAME"]
    }
    rec = {
        "jobName" : data["ETL_EXECUTION_ID"],
        "jobId" : data["jobId"],
        "startTime": data["time"],
        "time": curr_time,
        "status": data['STATUS'],
        "_documentType":"job",
    }
    rec['metaData'] = metadata
    rec.update(tags)
    if flag == 'started':
        rec['started'] = True
    else:
        rec['completed'] = True
        rec['endTime'] = data['time']
        if 'job' in bufferData.get(data['jobId']).keys():
            record = bufferData.get(data['jobId'])['job']
            rec['duration'] = data['time'] - record['startTime']
            rec['startTime'] = record['startTime']
        else:
            print("No job start record found")
    return rec

def form_stage_record(data, flag, tags):
    rec = {
        "jobName" : data["ETL_EXECUTION_ID"],
        "jobId" : data["jobId"],
        "startTime": data["time"],
        "time": int(time.time() * 1000),
        "status": data['STATUS'],
        "_documentType":"stage",
        "stageName": data['stageName']
    }
    rec.update(tags)
    if flag == 'started':
        rec['started'] = True
    else:
        record = bufferData.get(data['jobId']).get(data['stageName'])
        rec['duration'] = data['time'] - record['startTime']
        rec['endTime'] = data['time']
        rec['startTime'] = record['startTime']
        rec['completed'] = True
    return rec


def work(metricConfig, bufferPath):

    tags = {
        "_plugin": (metricConfig.get("metrics",{}).get("plugins")[0]).get("name"),
        "_tag_Name": metricConfig.get("tags").get("Name"),
        "_tag_appName": metricConfig.get("tags").get("appName"),
        "_tag_projectName": metricConfig.get("tags").get("projectName")
    }

    datalogs = get_data(metricConfig.get("metrics",{}).get("plugins")[0])
  
    # datalogs = ast.literal_eval(json.dumps(datalogs))
    datalogs = [iterateDict(i) for i in datalogs]

    # datalogs = [i for i in datalogs if i.get("job_id",0) == "854e0a8d-3125-44c2-935b-0e219ec262d992"]
    curr_time = int(time.time() * 1000) 
    
  
    def sort_by_time(data):
        return data['time']

    datalogs.sort(key=sort_by_time, reverse=False)
   
    started_rec = [x for x in datalogs if 'start' in x['STATUS'].lower()]
    completed_rec = [x for x in datalogs if 'start' not in x['STATUS'].lower()]
    

    started_records = {}
    completed_records = {}
    task_exclusion_list = ["1828591 MAIN INCR ETL", "1828594 E2B INCR ETL", "1828595 SET_START_PARAM", "1828599 SET_START_PARAM", "1830330 ETL_HOOK_POST_CDR_TRANSFORM-INCR", "TEMP_REPORTABILITY_FLAG", "1829247 ACTIVESUBSTANCE_ADDL", "1829244 PRIMARYSOURCE_ADDL", "1829241 LITERATUREREFERENCES_ADDL", "1829238 RECEIVER_ADDL", "1829235 MHLWADMICSRCASENUM_ADDL", "1829233 DRUGREACTIONRELATEDNESS_ADDL", "1829230 MHLWDUMMY_ADDL", "1829228 DRUG_ADDL", "1829225 DOSAGEINFORMATION_ADDL", "1829222 PATIENT_ADDL", "1829219 REACTION_ADDL", "1829979 T_IDENTIFICATION_FU", "1829975 T_IDENTIFICATION_FU", "1829967 S_IDENTIFICATION_FU", "1830287 CDR_PROD_AE_TTO"]
    completedJob = []
    with open(bufferPath, 'r') as f:
       bufferData = json.load(f)
    for data in started_rec:
        if data['jobId'] not in bufferData.keys():
            bufferData[data['jobId']] = {}
        jobId = data['jobId']
        if 'job' in bufferData.get(data['jobId']).keys():
            print("i1")
            record = bufferData.get(data['jobId'])['job']
            duration = data['time'] - record['startTime']
            print(duration)
        if data.get("TABLE_NAME","") == "INCR ETL":
            if 'job' not in bufferData[jobId].keys():
                record = form_job_record(data, 'started', tags, curr_time)
                started_records.update({jobId:record})
                bufferData[jobId].update({'job': record})
        else:
            if data.get("ID") is not None:
                taskId = str(int(data["ID"])) + ' ' + data["TABLE_NAME"]
            else:
                taskId = data["TABLE_NAME"]
            if taskId not in task_exclusion_list:
                record = form_task_record(data, 'started', tags, curr_time, taskId)
                if taskId not in bufferData.get(jobId).keys():
                    bufferData[jobId].update({taskId: record})
                    id_1 = data['jobId'] + '_' + taskId
                    started_records.update({id_1:record})
    for data in completed_rec:
        jobId = data['jobId']
        if data.get("TABLE_NAME","") == "INCR ETL":
            if data['jobId'] in started_records.keys():
                completed_record = started_records[jobId]
                completed_record['duration'] = data['time'] - completed_record['startTime']
                completed_record['time'] = curr_time
                completed_record['endTime'] = data['time']
                del completed_record['started']
                completed_record['status'] = data['STATUS']
                completed_record['completed'] = True        
                del started_records[jobId]
                completedJob.append(jobId)
                completed_records.update({jobId: completed_record}) 

            else:    
                record = form_job_record(data, 'completed', tags, curr_time, bufferData)
                completed_records.update({data['jobId']:record})
                completedJob.append(jobId)
            
        else:
            if data.get("ID") is not None:
                taskId = str(int(data["ID"])) + ' ' + data["TABLE_NAME"]
            else:
                taskId = data["TABLE_NAME"]
            id_1 = data['jobId'] + '_' + taskId
            if taskId not in task_exclusion_list:
                """
                Common records - directly insert completed records
                """
                new_task = data['jobId'] + '_' + taskId
                if new_task in started_records.keys():
                    if data['jobId'] == started_records.get(id_1)['jobId']:
                        completed_record = started_records[id_1]
                        completed_record['duration'] = data['time'] - completed_record['startTime']
                        completed_record['time'] = curr_time
                        completed_record['endTime'] = data['time']
                        del completed_record['started']
                        completed_record['status'] = data['STATUS']
                        completed_record['completed'] = True        
                        del started_records[id_1]
                        del bufferData[data['jobId']][taskId]
                        completed_records.update({id_1: completed_record}) 
                else:
                    rec = form_task_record(data, 'completed', tags, curr_time, taskId, bufferData)
                    if rec is not None:
                        del bufferData[data['jobId']][taskId]
                        completed_records.update({id_1: rec})

    for jobId in completedJob:
        taskKeys = bufferData.get(jobId).keys()
        for taskId in taskKeys:
            if taskId != 'job':
                id_1 = jobId + '_' + taskId
                rec = bufferData.get(jobId).get(taskId)
                rec['endTime'] = None
                rec['completed'] = True
                rec['duration'] = None
                rec['status'] = None
                completedJob = completed_records.get(jobId)
                rec['time'] = curr_time
                del rec['started']
                completed_records.update({id_1: rec})
        del bufferData[jobId]
    with open(bufferPath, "w") as fl:
        json.dump(bufferData,fl)
    for _, val in completed_records.items():
        write_docs_bulk(metricConfig, [val])
    
    for _, val in started_records.items():
        write_docs_bulk(metricConfig, [val])
