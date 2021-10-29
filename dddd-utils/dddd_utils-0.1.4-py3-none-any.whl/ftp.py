# -*- coding: utf-8 -*-
"""
操作FTP服务器
目前仅支持下载和删除
"""
__all__ = [
    'FtpDownload',
]

import os
import ftplib


class FtpDownload(object):
    def __init__(self, ip, port, user_name, pwd):
        self.ftpserver = ip  # ftp主机IP
        self.port = port  # ftp端口
        self.user_name = user_name  # 登陆用户名
        self.pwd = pwd  # 登陆密码
        self.ftp = self.ftp_connect()

    def ftp_connect(self):
        """ftp连接"""
        ftp = ftplib.FTP()
        try:
            ftp.connect(self.ftpserver, self.port)
            ftp.login(self.user_name, self.pwd)
        except:
            raise IOError('FTP login failed!!!')
        else:
            print(ftp.getwelcome())
            return ftp

    def download_file(self, ftp_file, local_file):
        """单个文件下载到本地"""
        try:
            self.ftp.pwd()
        except:
            self.ftp = self.ftp_connect()

        bufsize = 1024
        with open(local_file, 'wb') as fid:
            self.ftp.retrbinary('RETR {0}'.format(ftp_file), fid.write, bufsize)
        return True

    def download_files(self, ftp_path, local_path):
        """下载整个目录下的文件,包括子目录文件"""
        # print('FTP PATH: {0}'.format(ftp_path))
        if not os.path.exists(local_path):
            os.makedirs(local_path)

        try:
            self.ftp.pwd()
        except:
            self.ftp = self.ftp_connect()

        self.ftp.cwd(ftp_path)

        for i, file_name in enumerate(self.ftp.nlst()):
            if not file_name.endswith(".zip"):
                continue
            # print('{0} <> {1}'.format(i, file_name))
            local = os.path.join(local_path, file_name)

            if self.__is_filedir(file_name=file_name):  # 判断是否为子目录
                if not os.path.exists(local):
                    os.makedirs(local)
                self.download_files(file_name, local)
            else:
                self.download_file(file_name, local)
        self.ftp.cwd('..')
        return True

    def delete_file(self, ftp_dir, file_name):
        """删除文件夹中的所有文件"""
        try:
            self.ftp.pwd()
        except:
            self.ftp = self.ftp_connect()

        self.ftp.cwd(ftp_dir)
        current_file_list = self.ftp.nlst()
        if file_name in current_file_list:
            self.ftp.delete(file_name)
            print(f"{file_name} 删除成功")
        else:
            print(f"{file_name} 目标文件不存在")
        self.ftp.cwd('..')

    def delete_files(self, ftp_dir):
        """清空文件夹"""
        try:
            self.ftp.pwd()
        except:
            self.ftp = self.ftp_connect()
        self.ftp.cwd(ftp_dir)
        for file_name in self.ftp.nlst():
            if not file_name.endswith(".zip"):
                continue
            if self.__is_filedir(file_name=file_name):  # 判断是否为子目录
                self.delete_files(file_name)
            else:
                self.ftp.delete(file_name)

    def ftp_disconnect(self):
        """退出FTP连接"""
        self.ftp.quit()

    def __is_filedir(self, file_name):
        """
        判断是否是文件夹
        :param file_name: 文件名/文件夹名
        :return:返回字符串“File”为文件，“Dir”问文件夹，“Unknow”为无法识别
        """
        rec = ""
        try:
            rec = self.ftp.cwd(file_name)  # 需要判断的元素
            self.ftp.cwd("..")  # 如果能通过路劲打开必为文件夹，在此返回上一级
        except Exception as e:
            rec = e  # 不能通过路劲打开必为文件，抓取其错误信息
        finally:
            if "550 Failed to change directory" in str(rec):
                return False
            elif "Directory successfully changed." in str(rec):
                return True
            else:
                return False
