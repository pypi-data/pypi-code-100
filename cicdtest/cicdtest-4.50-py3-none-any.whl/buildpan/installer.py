"""
    Title: installer
    Author: Abizer
    Modified By: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 24-09-2021
    Description:
        ###############################################################
        ##      Calls platform installer to install node             ## 
        ###############################################################
 """

from buildpan import yaml_reader, platform_installer


def installer(project_id, repo_name, username):
    try:
        print("\nInstalling platform dependencies...")
        platform_name = yaml_reader.yaml_reader.platform_name
        node_ver = yaml_reader.yaml_reader.platform_ver

        if platform_name == "node":
            platform_installer.node_installer(node_ver, project_id, repo_name, username)
        elif platform_name == "":
            print("Error:- platform name is empty")
        else:
            print(f"Error:- {platform_name} is not supported")
    
    except Exception as e:
        print("Installer failed. Please see logs for more detail")