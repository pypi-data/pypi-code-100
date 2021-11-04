# coding=utf-8

"""
    @header akso.py
    @abstract   
    
    @MyBlog: http://www.kuture.com.cn
    @author  Created by Kuture on 2021/11/4
    @version 1.0.0 2021/11/4 Creation()
    
    @Copyright © 2021年 Mr.Li All rights reserved
"""
import os
import sys
import time
import shutil
import subprocess
from tqdm import tqdm


TEMP_LABEL = "KutureTemporaryDoNotUse"


# Cython Transform Class
class CythonTransform(object):

    def __init__(self, save_folder=None, python_exc='python', exclude_list=None):

        '''

        :param save_folder:  save folder path
        :param python_exc:   python running absolutely path
        :param exclude_list:   exclude python file
        '''

        print('Transform Init...')
        if (save_folder == None) or (not os.path.exists(save_folder)):
            raise Exception('Save Folder Path Is None Or Wrong : {}'.format(save_folder))
        if not isinstance(exclude_list, list):
            if exclude_list is None:
                exclude_list = []
            else:
                raise Exception('"exclude_list" Is Not List Type')

        # Trans And Save
        self.trans_folder = os.getcwd()
        self.save_folder = save_folder

        # Running Files
        self.python_exc = python_exc
        self.temp_trans_file = './.temp_trans.py'
        self.temp_trans_file_content = 'from distutils.core import setup\nfrom Cython.Build ' \
                                       'import cythonize\nsetup(ext_modules=cythonize("'

        # Generate .so file tail
        self.cython_tail_name = self._obtain_transform_file_tail()

        # Exclude List
        current_exc_file = os.path.realpath(sys.argv[0])
        exclude_list.append(current_exc_file)
        self.exclude_list = exclude_list

        print('Transform Folder: {}'.format(self.trans_folder))
        print('Save Folder: {}'.format(self.save_folder))
        print('Python exc: {}'.format(self.python_exc))
        print('Exclude List: {}'.format(self.exclude_list))
        print('Cython Tail: {}'.format(self.cython_tail_name))

    # Obtain Transform File Tail
    def _obtain_transform_file_tail(self):

        temp_file = '{}.py'.format(TEMP_LABEL)
        with open(temp_file, 'w') as sf:
            sf.write('# Kuture')

        print(temp_file)
        self._trans_cython_method(temp_file)

        current_list = os.listdir('./')
        tail_name = [x for x in current_list if x.startswith('{}.cpython'.format(TEMP_LABEL))][0]
        tail_name = tail_name[tail_name.index('.'):]

        if os.path.exists(temp_file):
            os.remove(temp_file)
            os.remove('{}.c'.format(TEMP_LABEL))
        if os.path.exists('{}{}'.format(TEMP_LABEL, tail_name)):
            os.remove('{}{}'.format(TEMP_LABEL, tail_name))

        return tail_name

    def _trans_cython_method(self, trans_file):

        with open(self.temp_trans_file, 'w') as sf:
            sf.write('{}{}"))'.format(self.temp_trans_file_content, trans_file))

        res = subprocess.Popen('{} {} build_ext --inplace'.format(self.python_exc, self.temp_trans_file), shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        res = [x for x in res.stdout.readlines() if
               x.decode().strip().startswith('Cython.Compiler.Errors.CompileError')]
        if len(res) == 0:
            return 0
        else:
            return 1

    # filters
    def file_filters(self, file_path):

        # filter file
        if (file_path in self.exclude_list) or \
                (file_path[file_path.rfind('.'):] in ['.o', '.c', '.so', '.pyc', '.gitignore']):
            return False
        # filter folder
        if len([False for x in ['.git', '.idea'] if file_path.count(x) > 0]) > 0:
            return False

        return True

    # generate folder file list
    def _generate_folder_list(self):

        print('Generate Folder File List...')
        python_file_list = []
        for root, dir, files in os.walk(self.trans_folder):
            for file in files:
                python_file_path = os.path.join(root, file)
                if self.file_filters(python_file_path):
                    python_file_list.append(python_file_path)

        return python_file_list

    # build python to .so
    def build_python_file(self):

        python_file_list = self._generate_folder_list()

        print('Start Transform...')
        result_label_list = ['Success: ', 'Error ']
        count = 0
        total_count = len(python_file_list)
        so_file_remove_list = []
        for file in python_file_list:
            start_time = time.time()
            try:
                if file.endswith('.py'):
                    # change cython file and .so file
                    res_count = self._trans_cython_method(file)
                    source_c_file = '{}.c'.format(file[:file.rfind('.py')])
                    source_so_file = '{}{}'.format(file[:file.rfind('.py')], self.cython_tail_name)

                    # save file and save folder path
                    save_file = file.replace(self.trans_folder, self.save_folder)  # python file path
                    save_so_file = source_so_file.replace(self.trans_folder, self.save_folder)  # save so file path
                    base_save_folder = os.path.dirname(save_file)  # save folder

                    # check save path
                    if not os.path.exists(base_save_folder):
                        os.makedirs(base_save_folder)

                    # if change success, delete .so file
                    if res_count == 0:
                        if os.path.exists(source_so_file):
                            shutil.copy(source_so_file, save_so_file)
                            if so_file_remove_list.count(source_so_file) == 0:
                                so_file_remove_list.append(source_so_file)
                        else:
                            shutil.copy(os.path.join(self.trans_folder, os.path.basename(source_so_file)), save_so_file)
                            so_file_path = os.path.join(self.trans_folder, os.path.basename(source_so_file))
                            if so_file_remove_list.count(so_file_path) == 0:
                                so_file_remove_list.append(so_file_path)
                    else:
                        shutil.copy(file, save_file)

                    # delete .c file
                    if os.path.exists(source_c_file):
                        os.remove(source_c_file)

                # keep other file
                else:
                    res_count = 0
                    save_stitic_file = file.replace(self.trans_folder, save_folder)
                    base_stitic_folder = os.path.dirname(save_stitic_file)
                    if not os.path.exists(base_stitic_folder):
                        os.makedirs(base_stitic_folder)
                    shutil.copy(file, save_stitic_file)

                speed_time = '{:.2f}'.format(time.time()-start_time)
                count += 1
                print('{}/{} {}{}{}{}s'.format(count, total_count, result_label_list[res_count],
                                              file, '-'*(150-len(file)), speed_time))
            except Exception as error:
                print('Error: {}'.format(error))

        print('Remove So File...')
        for so_file in tqdm(so_file_remove_list):
            os.remove(so_file)
        print('Remove Temporary Folder...')
        build_folder = os.path.join(self.trans_folder, 'build')
        if os.path.exists(build_folder):
            shutil.rmtree(build_folder)
        if os.path.exists(self.temp_trans_file):
            os.remove(self.temp_trans_file)
