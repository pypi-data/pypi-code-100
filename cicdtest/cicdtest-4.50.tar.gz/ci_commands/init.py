
"""
    Title: init.py
    Author: Akash D.
    Modified By: Kushagra A.
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 21-09-2021
    Description:
        ###############################################################
        ## Starting file   ## 
         ###############################################################
 """

import requests
import json
import pathlib
import datetime
import click
from buildpan import github_webhook, bitbucket_webhook, encrypt
from buildpan import setting, yaml_reader
from pyfiglet import Figlet


info = setting.info

# getting env variable
fetch_log = info["FETCH_LOG_URL"]
         
@click.command()
def init():
    '''
    For initiating CI-CD operation  
    \f
   
    '''

    f = Figlet(font='slant')
    print (f.renderText('Buildpan'))

    path=pathlib.Path().resolve()
    print("Your current directory  is : ", path)
    try:

        yaml_reader.yaml_reader(path)
        
        project_id = yaml_reader.yaml_reader.project_id
        
        response = requests.get("https://app.buildpan.com/api/v1/projects/detail/"+project_id)
        data = response.json()

        provider = data['project']["provider"]

        enc_key = b'CgOc_6PmZq8fYXriMbXF0Yk27VT2RVyeiiobUd3DzR4='

        curtime = datetime.datetime.now()

        # github access
        if provider == "github":
            print("\nConnecting to remote repository...")

            name = data["project"]["repo"]["full_name"].split('/')
            token = data["project"]["repo"]["access_token"]
            username = name[0]
            repo_name = name[1]
            
            try:

                dictionary ={
                    "token" : token,
                    "username" : username,
                    "repo_name" : repo_name,
                }

                # Serializing json 
                json_object = json.dumps(dictionary, indent = 4)
            
                # Writing to sample.json
                with open(project_id+'.json',"w") as outfile:
                    outfile.write(json_object)
                
                #Reading from json file
                with open(project_id+'.json') as file:
                    info = json.load(file)
                    username = info["username"]
                    token = info["token"]
                    repo_name = info["repo_name"]
                
                # encrypting a json file
                enc = encrypt.Encryptor()
                enc.encrypt_file(enc_key, project_id+'.json')

                requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=initialization performed for github - '+repo_name+'&status=success&operation=init')

                github_webhook.github(project_id, path, token, username, repo_name, provider)
            except Exception as e:
                requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=initialization performed for github - '+repo_name+' failed.'+str(e)+'&status=failed&operation=init')
            
        # bitbucket access
        elif provider == "bitbucket":
            print("\nConnecting to remote repository...")
            
            name = data["project"]["repo"]["full_name"].split('/')
            token = data["project"]["repo"]["refresh_token"]
            username = name[0]
            repo_name = name[1]

            try:
                dictionary ={
                    "refresh_token" : token,
                    "username" : username,
                    "repo_name" : repo_name,
                }
                # Serializing json 
                json_object = json.dumps(dictionary, indent = 4)
                
                # Writing to sample.json
                with open(project_id+'.json',"w") as outfile:
                    outfile.write(json_object)
                
                # Reading from json file
                with open(project_id+'.json') as file:
                    info = json.load(file)
                    username = info["username"]
                    refresh_token = info["refresh_token"]
                    repo_name = info["repo_name"]

                # encrypting a json file
                enc = encrypt.Encryptor()
                enc.encrypt_file(enc_key, project_id+'.json')

                requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=initialization performed for bitbucket - '+repo_name+'&status=success&operation=init')
                
                bitbucket_webhook.bitbucket(project_id, path, refresh_token, username, repo_name, provider)
            except Exception as e:
                requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=initialization performed for bitbucket - '+repo_name+' failed.'+str(e)+'&status=failed&operation=init')
     
            

          
    except Exception as e:
        print("config file not found or not in proper format.")
        print("Message : " + str(e))
        print("Initialization failed")
        try:
            requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name= &Time='+str(curtime)+'&user_name= &message=initialization failed.'+str(e)+'&status=failed&operation=init')
        except:
            pass


