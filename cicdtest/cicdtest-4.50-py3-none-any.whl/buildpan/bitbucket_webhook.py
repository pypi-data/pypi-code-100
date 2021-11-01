
"""
    Title: bitbucket_webhook.py
    Author: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 23-09-2021
    Description:
        ###############################################################
        ## Create a webhook on a specific bitbucket repository   ## 
         ###############################################################
 """

import requests
import requests, datetime
from buildpan import create_file, installer
from buildpan import setting, access_token

info = setting.info

fetch_log = info["FETCH_LOG_URL"]
host = info["HOST"]

         
def bitbucket(project_id, path, refresh_token, username, repo_name, provider):
    try:
        print("\nCreating a webhook...")

        token = access_token.access_token(refresh_token)

        header = {
            "Authorization": 'Bearer ' + token,
            'Content-Type': 'application/json',

        }
        
        curtime = datetime.datetime.now()
        # creating a webhook on a particular repository
        hook_url = f"https://api.bitbucket.org/2.0/repositories/{username}/{repo_name}/hooks"
        payload_url = f"http://{host}/bit_webhook"

        response3 = requests.get(hook_url, headers=header)
        data = response3.json()['values']
        hook_body = {
            "description": "Webhook Description",
            "url": payload_url,
            "active": True,
            "events": [
                "repo:push",
                "repo:commit_comment_created",
            ]
        }
        uuid = None

        for value in data:
            url = value["url"]

            if payload_url != url or len(data) == 0:
                requests.post(hook_url, headers=header, json=hook_body)

                print("Creating webhook done")
                requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=webhook created for repository - '+repo_name+'&status=success&operation=webhook')

                installer.installer(project_id, repo_name, username)

                # create file
                create_file.create_file(project_id, repo_name, path, username, provider)
                print("\nInit operation done.")
                break

            else:
                uuid = data[0]["uuid"][1:-1]
                url4 = hook_url + f"/{uuid}"                

                requests.put(url4, headers=header, json=hook_body)
                print("Webhook already exists")

                requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=Exception: webhook already exists for repository - '+repo_name +'&status=success&operation=webhook')

                installer.installer(project_id, repo_name, username)

                # create file
                create_file.create_file(project_id, repo_name, path, username, provider)
                print("\nInit operation done.")
                break
          
    except Exception as e:
        print("Initialization failed")
        requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=Exception: webhook creation failed for repository - '+repo_name+ '. '+ str(e)+'&status=failed&operation=webhook')
