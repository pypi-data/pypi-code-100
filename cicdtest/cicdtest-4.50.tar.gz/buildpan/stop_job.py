"""
    Title: stop_job
    Author: Kushagra A.
    Modified By: Kushagra A.
    Language: Python
    Date Created: 27-09-2021
    Date Modified: 27-09-2021
    Description:
        ###############################################################
        ##      Remove buildpan cron job                             ## 
        ###############################################################
"""

from crontab import CronTab

def stop_job():
    cron_job = CronTab(user=True)
    jobs= cron_job.find_comment('buildpan')
    jobs_list = list(jobs)
    if len(jobs_list) == 0:
        print("No buildpan operation is runnig!!\nRun:- buildpan start to intiate buildpan operation")
    else:
        for job in jobs_list:
            cron_job.remove(job)
            cron_job.write()
        print("buildpan operation successfully stopped!\nRun:- buildpan start to intiate buildpan operation")
    