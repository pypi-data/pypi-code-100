"""
    Title: platforminstaller
    Module Name: platforminstaller
    Author: Abizer
    Modified By: Abizer, Kushagra A.
    Language: Python
    Date Created: 4-09-2021
    Date Modified: 24-09-2021
    Description: diffrent platform installer to be called at init process  
        ###############################################################
        ##                 platform installer                        ## 
        ###############################################################
 """
import subprocess
import sys
from buildpan import setting
import datetime, requests

info = setting.info


fetch_log = info["FETCH_LOG_URL"]


def node_installer(node_ver, project_id, repo_name, username):
    '''
    node installer this function to be called for Linux machine 

    '''
    try:
        client_os=sys.platform
        curtime = datetime.datetime.now()

        if client_os == "linux":
            subprocess.run("curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash", shell= True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.run("source ~/.nvm/nvm.sh", shell= True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,executable='/bin/bash')

            popen_arg = "nvm install "+ node_ver 
            subprocess.call(['/bin/bash', '-i', '-c', popen_arg])
            requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=Installer installed'+'&status=success&operation=platform installer')

            if node_ver != "latest":
                popen_arg = "nvm use "+ node_ver
                subprocess.call(['/bin/bash', '-i', '-c', popen_arg])
        
        elif client_os == "win32" or client_os == "cygwin":
            popen_arg = "nvm install "+ node_ver 
            result = subprocess.run(popen_arg ,shell= True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=Installer : '+str(result.stdout.decode())+'&status=success&operation=platform installer')
            

            if node_ver != "latest":
                popen_arg = "nvm use "+ node_ver
                subprocess.run(popen_arg ,shell= True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    except Exception as e:
        requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=Installer : '+str(e)+'&status=failed&operation=platform installer')
    
