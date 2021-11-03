#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : simple_web
# @Time         : 2021/10/26 下午7:13
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : tar -cvf [目标文件名].tar [原文件名/目录名]


from appzoo import App

app = App()

app.add_route('/', lambda **kwargs: kwargs)  # values.get_value()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
