"""
    Title: stop_all
    Author: Kushagra A.
    Modified By: Kushagra A.
    Language: Python
    Date Created: 27-09-2021
    Date Modified: 27-09-2021
    Description:
        ###############################################################
        ##      Remove all repo details from centralized file        ## 
        ###############################################################
"""


import click
from click.decorators import command
from crontab import CronTab
import os

@click.command()
def restart():
    '''
     For restart CI-CD operation
    \f
    
   
    '''
    try:
        PATH = os.getenv("PATH")

        cron_job = CronTab(user=True)
        jobs= cron_job.find_comment('buildpan')
        jobs_list = list(jobs)
        response = False
        if len(jobs_list) == 0:
            print("No buildpan operation is runnig!!\n Run:- 'buildpan start' to intiate buildpan operation")
            response = False
        else:
            for job in jobs_list:
                cron_job.remove(job)
            response = True

        if response == True:
                job = cron_job.new(command=f'export PATH=$PATH:{PATH} && buildpan pull', comment = 'buildpan')
                job.minute.every(2)
                cron_job.write()
    except Exception as e:
        print("exception = " + e)

