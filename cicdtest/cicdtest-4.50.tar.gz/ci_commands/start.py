"""
    Title: start.py
    Author: Kushagra A.
    Language: Python
    Date Created: 10-09-2021
    Date Modified: 21-09-2021
    Description:
        ###############################################################
        ## Create a cron process   ## 
         ###############################################################
 """


import click
from click.decorators import command
from crontab import CronTab
import os


@click.command()
def start():
    '''
    To start Buildpan CI-CD operation  

    \f
    '''
    try:
        PATH = os.getenv("PATH")
        cron_job = CronTab(user=True)
        jobs = cron_job.find_comment('buildpan')
        if len(list(jobs))==0:
            job = cron_job.new(command=f'export PATH=$PATH:{PATH} && buildpan pull', comment = 'buildpan')
            job.minute.every(2)
            cron_job.write()
        else:
            print("Buildpan operation is already running.\n Run:- buildpan init to start CI-CD operation.")
    except Exception as e:
        print(e)