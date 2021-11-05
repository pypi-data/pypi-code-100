# coding=utf-8

"""
    @header akso.py
    @abstract   
    
    @MyBlog: http://www.kuture.com.cn
    @author  Created by Kuture on 2021/11/4
    @version 1.0.0 2021/11/4 Creation()
    
    @Copyright © 2021年 Mr.Li All rights reserved
"""

from aksoso._akso_ import AKSoTransform


class AKSo(AKSoTransform):

    def __init__(self, save_folder=None, python_exc='python', exclude_list=None):
        super(AKSo, self).__init__(save_folder=save_folder, python_exc=python_exc, exclude_list=exclude_list)

    def build(self):

        self.build_python_file()

