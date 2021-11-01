

"""
    Title: version.py
    Author: Akash Dwivedi
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 14-08-2021
    Description:
        ###############################################################
        ## Checks the version of the cli  ## 
         ###############################################################
 """
import click
from buildpan import setting


info = setting.info




@click.command()
def version():
    '''
    Display the current version of the buildpan
    '''

    version = info["version"]
    
    print(f'Current Buildpan version is {version}')