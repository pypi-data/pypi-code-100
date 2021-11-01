"""
    Title: deployer
    Module Name: deployer
    Author: Abizer
    Modified By: Abizer, Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 22-09-2021
    Description: Return Type is Bolean Is success then "True" otherwise "False"
        ###############################################################
        ##                 Deployer for all Stack                    ## 
        ###############################################################
 """

import subprocess 
import datetime, requests
import json
import os, time
from buildpan import setting

info = setting.info


fetch_log = info["FETCH_LOG_URL"]

def mean_stack(cwd, project_id, repo_name, username):
    '''
    Deploy MeanStack project
    '''
    try:

        success = False
        curtime = datetime.datetime.now()
        message = ""
        
        # Reding entrypoint 
        file_path = os.path.join(cwd,"package.json")
        package_file = open(file_path)
        project_detail = json.loads(package_file.read())
        package_file.close()

        # installing all the dependency if packge.json found otherwise genrate error
        result_install = subprocess.run(['npm', 'install'] , stdout= subprocess.PIPE, stderr = subprocess.STDOUT, cwd=cwd)
        if result_install.returncode:
            requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=deployment = '+str(result_install.stdout.decode())+'&status=failed&operation=deployment')
            return success 
        else:
            # if pm2 is not installed installing otherwise update 
            result_install_pm2 = subprocess.run(['npm','install', 'pm2', '-g'], stdout= subprocess.PIPE, stderr = subprocess.PIPE)
            if result_install_pm2.returncode:
                requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=deployment = '+str(result_install.stdout.decode())+'&status=failed&operation=deployment')
                return success
            else:

                # check service status if off start that otherwise reload it 
                service_status = subprocess.run(['pm2', 'status'], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                if service_status.stdout.decode().find("online") == -1:
                    popen_arg = ['pm2', 'start', '--name', project_id, "--namespace", "buildpan", "npm","--", "start"]
                    result_start = subprocess.run(popen_arg, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, cwd = cwd)
                    process_fails = result_start.returncode
                    message = result_start.stdout.decode()
                else:
                    popen_arg = ['pm2', 'reload', project_id]
                    result_relod = subprocess.run(popen_arg, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, cwd = cwd)
                    process_fails = result_relod.returncode
                    message = result_relod.stdout.decode()

                    if process_fails:
                        popen_arg = ["pm2", "start", '--name', project_id, "--namespace", "buildpan", "npm","--", "start"]
                        result_start = subprocess.run(popen_arg, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, cwd = cwd)
                        process_fails = result_start.returncode
                        message = result_start.stdout.decode()

            if process_fails:
                requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=deployment = '+str(message)+'&status=failed&operation=deployment')
                return success
            else: 
                success = True
                time.sleep(4)
                show = subprocess.run(["pm2", "desc", project_id], stdout= subprocess.PIPE, stderr = subprocess.STDOUT)
                decode = show.stdout.decode()
                status = decode.find("status")
                add = status + 20
                msg = decode[add:160].strip()
                post_data = fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=deployment = '+str(message)+'&status='+str(msg)+'&operation=deployment'
                requests.post(post_data)
                return success
    except Exception as e:
        requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=Exception: deployment = '+str(e)+'&status=failed&operation=deployment')
        return False

def script_runer(scripts, path):
    '''
    Script runner is called when Script under jobs is called in workflow and have some script 
    that to be executed 
    
    '''
    
    success = False
    for script in scripts:
        script_list = list(script.split(" "))
        result = subprocess.run(script_list,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd = path)
        print(result.stdout.decode())
        if result.returncode:
            return success
        
    success = True
    return success
    
            



