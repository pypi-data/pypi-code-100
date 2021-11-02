# -*- coding: utf-8 -*
def run_hive(sql,host1,host2,port,username,message,url):
    from pyhive import hive
    import requests
    import json
    import re
    import sys
    try:
        sqls='''set hive.tez.auto.reducer.parallelism=true;
        set hive.exec.reducers.max=99;
        set hive.merge.tezfiles=true;
        set hive.merge.smallfiles.avgsize=32000000;
        set hive.merge.size.per.task=128000000;
        set tez.queue.name=analyst;'''+sql
        sqllist = [j for j in sqls.split(';') if j != '']
        res=[]
        conn = hive.connect(host=host1,port=port,username=username)
        cursor = conn.cursor()
        for i in sqllist:
            cursor.execute(i)
            try:
                res = cursor.fetchall()
            except:
                pass
            conn.commit()
        conn.close()
        return res
    except:
        try:
            conn = hive.connect(host=host2,port=port,username=username)
            cursor = conn.cursor()
            for i in sqllist:
                cursor.execute(i)
                try:
                    res = cursor.fetchall()
                except:
                    pass
                conn.commit()
            conn.close()
            return res
        except Exception as e:
            try:
                error='告警消息: '+message+'\n'+i+'\n'+re.match(r'.* (FAILED:.*)',str(e)).group(1)
            except:
                error='告警消息: '+i+'\n'+str(e)
            finally:
                headers = {'Content-Type': 'application/json'}
                data={
                    "msgtype": "text",
                    "text": {
                        "content": error,
                    }
                }
                response=requests.post(url,data=json.dumps(data),headers=headers)
                sys.exit()
                
def send_alert(message,url):
    import requests
    import json
    message='提示消息: '+str(message)
    headers = {'Content-Type': 'application/json'}
    data={
        "msgtype": "text",
        "text": {
            "content": message,
        }
    }
    response=requests.post(url,data=json.dumps(data),headers=headers)




   
                
