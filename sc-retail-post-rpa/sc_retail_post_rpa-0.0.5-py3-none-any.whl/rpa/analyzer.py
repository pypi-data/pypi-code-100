#  The MIT License (MIT)
#
#  Copyright (c) 2021. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
import logging
import os
from datetime import datetime
from shutil import copy2
from time import sleep, time

from config42 import ConfigManager
from dateutil.relativedelta import relativedelta
from sc_retail_analysis.main import main as retail_main


class RpaAnalyzer:
    """
    RPA分析流程
    """

    def __init__(self, *, config: ConfigManager):
        self._config = config
        # 需要下载的文件列表
        self._download_file_list = list()
        # 除了上述下载文件列表外，数据分析依赖的其他文件列表
        self._other_analysis_file_list = list()
        self._read_config()

    def ensure_dir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def _read_config(self):
        """
        读取配置文件
        """
        logging.getLogger(__name__).info("读取配置文件...")
        # 数据分析文件存放根路径
        self._analysis_root_directory = self._config.get("retail_rpa.analysis_root_directory")
        # 日期文件夹格式
        self._date_directory_format = self._config.get("retail_rpa.date_directory_format")
        # 文件下载路径
        self._download_directory = self._config.get("retail_rpa.download_directory")
        # 需要下载的文件列表
        download_file_list = self._config.get("retail_rpa.download_file_list")
        if download_file_list is not None and len(download_file_list) > 0:
            self._download_file_list.extend(download_file_list)
        # 除了上述下载文件列表外，数据分析依赖的其他文件列表
        other_analysis_file_list = self._config.get("retail_rpa.other_analysis_file_list")
        if other_analysis_file_list is not None and len(other_analysis_file_list) > 0:
            self._other_analysis_file_list.extend(other_analysis_file_list)
        # 检查文件清单的时间间隔（单位：秒）
        self._checking_time_interval = self._config.get("retail_rpa.checking_time_interval")
        # 检查文件清单的时间最大值（单位：秒）
        self._checking_time_threshold = self._config.get("retail_rpa.checking_time_threshold")
        # 分析的配置文件模板路径
        self._template_analysis_config_filepath = self._config.get("retail_rpa.template_analysis_config_filepath")
        # 花名册文件模板路径
        self._template_manifest_filepath = self._config.get("retail_rpa.template_manifest_filepath")

    def _check_config(self) -> bool:
        """
        检查配置项
        """
        logging.getLogger(__name__).info("检查配置项...")
        if self._analysis_root_directory is None:
            logging.getLogger(__name__).error("'数据分析文件存放根路径'未配置")
            return False
        if not os.path.exists(self._analysis_root_directory):
            logging.getLogger(__name__).error(f"'数据分析文件存放根路径' {self._analysis_root_directory} 文件夹不存在")
            return False
        if not os.path.isdir(self._analysis_root_directory):
            logging.getLogger(__name__).error(f"'数据分析文件存放根路径' {self._analysis_root_directory} 不是文件夹")
            return False
        today = datetime.today()
        yesterday = today - relativedelta(days=1)
        self._yesterday = yesterday.strftime(self._date_directory_format)
        # 数据分析文件夹
        self._analysis_directory = os.path.join(self._analysis_root_directory, self._yesterday)
        if self._download_directory is None:
            logging.getLogger(__name__).error("'文件下载路径'未配置")
            return False
        if not os.path.exists(self._download_directory):
            logging.getLogger(__name__).error(f"'文件下载路径' {self._download_directory} 文件夹不存在")
            return False
        if not os.path.isdir(self._download_directory):
            logging.getLogger(__name__).error(f"'文件下载路径' {self._download_directory} 不是文件夹")
            return False
        if self._template_analysis_config_filepath is None:
            logging.getLogger(__name__).error("'分析的配置文件模板路径'未配置")
            return False
        if not os.path.exists(self._template_analysis_config_filepath):
            logging.getLogger(__name__).error(f"'分析的配置文件模板路径' {self._template_analysis_config_filepath} 文件不存在")
            return False
        if not os.path.isfile(self._template_analysis_config_filepath):
            logging.getLogger(__name__).error(f"'分析的配置文件模板路径' {self._template_analysis_config_filepath} 不是文件")
            return False
        if self._template_manifest_filepath is None:
            logging.getLogger(__name__).error("'花名册文件模板路径'未配置")
            return False
        if not os.path.exists(self._template_manifest_filepath):
            logging.getLogger(__name__).error(f"'花名册文件模板路径' {self._template_manifest_filepath} 文件不存在")
            return False
        if not os.path.isfile(self._template_manifest_filepath):
            logging.getLogger(__name__).error(f"'花名册文件模板路径' {self._template_manifest_filepath} 不是文件")
            return False
        if len(self._download_file_list) == 0:
            logging.getLogger(__name__).error("'需要下载的文件列表' 配置为空")
            return False
        if len(self._other_analysis_file_list) == 0:
            logging.getLogger(__name__).error("'数据分析依赖的其他文件列表' 配置为空")
            return False
        if self._checking_time_interval is None:
            logging.getLogger(__name__).error(f"'检查文件清单的时间间隔' 未配置")
            return False
        interval_min = 10
        interval_max = 120
        if self._checking_time_interval < interval_min or self._checking_time_interval > interval_max:
            logging.getLogger(__name__).error(
                f"'检查文件清单的时间间隔' {self._checking_time_interval} 配置不合理，"
                f"应该位于{interval_min} 至 {interval_max} 区间"
            )
            return False
        if self._checking_time_threshold is None:
            logging.getLogger(__name__).error(f"'检查文件清单的时间间隔' 未配置")
            return False
        threshold_min = 60 * 60
        threshold_max = 180 * 60
        if self._checking_time_threshold < threshold_min or self._checking_time_threshold > threshold_max:
            logging.getLogger(__name__).error(
                f"'检查文件清单的时间最大值' {self._checking_time_threshold} 配置不合理，"
                f"应该位于{threshold_min} 至 {threshold_max} 区间"
            )
            return False
        return True

    def _check_if_all_files_downloaded(self) -> bool:
        """
        检测报表文件是否下载齐全
        """
        logging.getLogger(__name__).info("检测报表文件是否下载齐全...")
        for target_file in self._download_file_list:
            full_path = os.path.join(self._download_directory, target_file)
            if not os.path.exists(full_path):
                logging.getLogger(__name__).error(f"下载文件 {full_path} 不存在")
                return False
        return True

    def _copy_downloaded_files(self):
        """
        将下载的文件复制到分析文件夹
        """
        logging.getLogger(__name__).info("将下载的文件复制到分析文件夹...")
        # 确保分析文件夹存在，如果不存在则创建
        self.ensure_dir(self._analysis_directory)
        for src_file in self._download_file_list:
            full_path = os.path.join(self._download_directory, src_file)
            copy2(src=full_path, dst=self._analysis_directory)
        return 0

    def _copy_other_files(self):
        """
        将其他文件复制到分析文件夹
        """
        logging.getLogger(__name__).info("将其他文件复制到分析文件夹...")
        # 确保分析文件夹存在，如果不存在则创建
        self.ensure_dir(self._analysis_directory)
        other_file_list = list()
        other_file_list.append(self._template_analysis_config_filepath)
        other_file_list.append(self._template_manifest_filepath)
        for src_file in other_file_list:
            copy2(src=src_file, dst=self._analysis_directory)
        return 0

    def _check_if_all_dependent_files_existed(self) -> bool:
        """
        检测数据分析依赖的文件是否到齐
        """
        logging.getLogger(__name__).info("检测数据分析依赖的文件是否到齐...")
        all_files = list()
        all_files.extend(self._download_file_list)
        all_files.extend(self._other_analysis_file_list)
        for target_file in all_files:
            full_path = os.path.join(self._analysis_directory, target_file)
            if not os.path.exists(full_path):
                logging.getLogger(__name__).error(f"依赖文件 {full_path} 不存在")
                return False
        return True

    def _run_retail_analysis(self):
        """
        运行数据分析
        """
        logging.getLogger(__name__).info("运行数据分析...")

        original_path = os.getcwd()
        dirname = self._analysis_directory
        logging.getLogger(__name__).info(f"切换到分析文件夹：{dirname}")
        os.chdir(dirname)
        result = retail_main()
        os.chdir(original_path)
        return result

    def analysis(self):
        """
        RPA之后的分析流程
        """
        if not self._check_config():
            logging.getLogger(__name__).error("配置文件检查失败，无法进行分析，程序退出")
            return 1
        if not self._check_if_all_files_downloaded():
            logging.getLogger(__name__).error("文件下载不齐全，无法进行分析，程序退出")
            return 1

        result = self._copy_downloaded_files()
        if result != 0:
            return result
        result = self._copy_other_files()
        if result != 0:
            return result

        all_dependent_file_existed = False
        # 循环检测依赖文件是不齐全
        check_start_time = time()
        while True:
            if self._check_if_all_dependent_files_existed():
                # 如果找到所有的文件则退出检测
                all_dependent_file_existed = True
                break
            current_time = time()
            checked_time = current_time - check_start_time
            if checked_time > self._checking_time_threshold:
                # 超时退出检测
                break
            sleep(self._checking_time_interval)

        if not all_dependent_file_existed:
            logging.getLogger(__name__).error("依赖的文件不齐全，无法进行分析，程序退出")
            return 1

        logging.getLogger(__name__).error("依赖的文件齐全，开始进行分析")
        return self._run_retail_analysis()
