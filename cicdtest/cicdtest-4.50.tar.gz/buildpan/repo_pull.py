"""
    Title: repo_pull.py
    Author: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 23-09-2021
    Description:
        ###############################################################
        ## Perform a pull operation on a repository   ## 
         ###############################################################
 """

import datetime
import requests
from buildpan import setting, access_token, read_file
import subprocess


info = setting.info


fetch_log = info["FETCH_LOG_URL"]


def repo_pull(path, project_id, repo_name, username, provider):

    try:
        curtime = datetime.datetime.now()

        if provider == "github":
            result = subprocess.call(["git", "pull", "origin", "main"], cwd=path)

            requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=pull operation performed'+'&status=success&operation=pull')

        elif provider == "bitbucket":
            refresh_token = read_file.read_file(path, project_id)
            token = access_token.access_token(refresh_token)

            pull = ["git", "-c", f"http.extraHeader=Authorization: Bearer {token}", "pull", "origin", "master"]

            result = subprocess.run(pull, stdout= subprocess.PIPE, stderr = subprocess.STDOUT, cwd=path)

            if result.returncode == 0:
                requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=pull operation performed : '+str(result.stdout.decode())+'&status=success&operation=pull')
            else:
                requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=pull operation performed : '+str(result.stdout.decode())+'&status=failed&operation=pull')
    
    except Exception as e:
        curtime = datetime.datetime.now()          
        requests.post(fetch_log+ "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=Exception: pull operation performed. '+str(e)+'&status=failed&operation=pull')
