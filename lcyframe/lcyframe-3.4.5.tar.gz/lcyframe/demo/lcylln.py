# -*- coding:utf-8 -*-
import json
import tornado.httpserver
import tornado.ioloop
from tornado.web import RequestHandler, Application
import tornado.options
from tornado.options import define, options
from tornado.escape import json_decode, json_encode
import random, time
# tasks.py
from celery import Celery



app = Celery('tasks', backend='redis://localhost:3379/0',
             broker='redis://localhost:3379/0')  # 配置好celery的backend和broker

from celery import Task

class DebugTask(Task):
    abstract = True

    def after_return(self, *args, **kwargs):
        print('Task returned: {0!r}'.format(self.request))

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print("on_failure(self, exc, task_id, args, kwargs, einfo)")

@app.task(base=DebugTask)
def add(x, y):
    return x + y

@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5}, base=DebugTask)
def test_func(self):
    print(1111)
    raise Exception()


if __name__ == "__main__":
    # send_wx_text('a')
    print(add(1, 2))
    print(test_func())