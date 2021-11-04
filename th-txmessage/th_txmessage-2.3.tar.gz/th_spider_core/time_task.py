from apscheduler.schedulers.blocking import BlockingScheduler
# 输出时间


class ThSchedulers:
    jobs = [];

    def add_jobs(self,**kwargs):
        def inner_function(func):
                self.jobs.append((func,kwargs));
        return inner_function;

    def __init__(self) -> None:
        self.scheduler = BlockingScheduler()

        
    def start(self):
        for item in self.jobs:
            self.scheduler.add_job(item[0], 'cron', **item[1]);
        self.scheduler.start()

