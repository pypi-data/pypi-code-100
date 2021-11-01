"""
    Title: stop
    Author: Kushagra A.
    Modified By: Kushagra A.
    Language: Python
    Date Created: 22-09-2021
    Date Modified: 21-09-2021
    Description:
        ###############################################################
        ## Remove a particular repo details from centralized file    ## 
        ###############################################################
"""

import click
from click.decorators import command
import os, pathlib
from buildpan import yaml_reader, find_path

@click.command()
def stop():
    '''
    For stop CI-CD operation for particular repository
    \f
    
   
    '''
    try:
        path=pathlib.Path().resolve()
        
        yaml_reader.yaml_reader(path)    
        project_id = yaml_reader.yaml_reader.project_id

        find_path.find_path()
        file_path = find_path.find_path.file_path
        
        try:
            with open(file_path + "/info.txt", "r") as input:
                with open(file_path + "/sample.txt", "w") as output:
                    for line in input:
                        data = eval(line)

                        # if substring contain in a line then don't write it
                        if project_id not in data["project_id"]:
                            output.write(str(data) + "\n")

                #replace file with original name
                os.replace(file_path +'/sample.txt', file_path +'/info.txt')
                print("CI-CD operation stopped on this repository\nRun:- buildpan init to initiate CI-CD operation")
        except:
            print("CI-CD operation already stopped on this repository\nRun:- buildpan init to initiate CI-CD operation")
    except:
        print("This repository is not configured.")