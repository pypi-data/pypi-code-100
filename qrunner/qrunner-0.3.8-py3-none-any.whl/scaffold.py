import os.path
import sys


def init_parser_scaffold(subparsers):
    sub_parser_scaffold = subparsers.add_parser(
        "startproject", help="Create a new project with template structure."
    )
    sub_parser_scaffold.add_argument(
        "project_name", type=str, nargs="?", help="Specify new project name."
    )
    return sub_parser_scaffold


def create_scaffold(project_name):
    """ create scaffold with specified project name.
    """

    def create_folder(path):
        os.makedirs(path)
        msg = f"created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"created file: {path}"
        print(msg)

    demo_run = """
import argparse
import pytest
from conf.config import conf


# 获取命令行输入的数据
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--serial_no', dest='serial_no', type=str, default='', help='设备id')
parser.add_argument('-p', '--pkg_name', dest='pkg_name', type=str, default='', help='应用包名')
parser.add_argument('-l', '--pkg_url', dest='pkg_url', type=str, default='', help='安装包路径')
parser.add_argument('-i', '--install', dest='install', type=str, default='no', help='是否需要重新安装, yes or no')

# 将数据写入配置文件
args = parser.parse_args()
conf.set_name('device', 'serial_no', args.serial_no)
conf.set_name('app', 'pkg_name', args.pkg_name)
conf.set_name('app', 'need_install', args.install)
conf.set_name('app', 'pkg_url', args.pkg_url)

# 执行用例
pytest.main(['tests', '--reruns', '1 ', '-s', '-v', '--alluredir', 'allure-results',
             '--clean-alluredir', '--html=report.html', '--self-contained-html'])
"""
    demo_conftest_adr = """
import pytest
from qrunner.core.android.element import driver
from qrunner.utils.log import logger
from conf.config import conf


# 安装应用
@pytest.fixture(scope='session', autouse=True)
def install_app():
    if conf.get_name('app', 'need_install') == 'yes':
        pkg_url = conf.get_name('app', 'pkg_url')
        logger.info(f'安装应用: {pkg_url}')
        driver.install_app(pkg_url, is_new=True)
    else:
        logger.info('无需重装应用')


# 初始化应用
@pytest.fixture(scope='session', autouse=True)
def init_app(install_app):
    if conf.get_name('app', 'need_install') == 'yes':
        pass
    else:
        logger.info('无需初始化')


# 用例的前置和后置操作
@pytest.fixture(scope='function', autouse=True)
def init_case():
    # 启动应用
    logger.info('启动应用')
    driver.force_start_app()
    yield
    # 截图
    driver.allure_shot('用例结束')
    # 停止应用
    logger.info('停止应用')
    driver.stop_app()
"""
    demo_conftest_ios = """
import pytest
from qrunner.utils.log import logger
from conf.config import conf
from qrunner.core.ios.element import driver

# 安装应用
@pytest.fixture(scope='session', autouse=True)
def install_app():
    if conf.get_name('app', 'need_install') == 'yes':
        pkg_url = conf.get_name('app', 'pkg_url')
        logger.info(f'安装应用: {pkg_url}')
        driver.install_app(pkg_url, is_new=True)
    else:
        logger.info('无需安装应用')

# 初始化权限
@pytest.fixture(scope='session', autouse=True)
def init_app(install_app):
    if conf.get_name('app', 'need_install') == 'yes':
        pass
    else:
        logger.info('无需初始化应用')

# 用例的前置和后置操作
@pytest.fixture(scope='function', autouse=True)
def init_case():
    # 启动应用
    logger.info('用例开始: 启动应用')
    driver.force_start_app()
    yield
    # 截图
    logger.info('用例结束: 进行截图')
    driver.allure_shot('用例结束')
    # 停止应用
    logger.info('用例结束: 退出应用')
    driver.stop_app()
"""

    demo_conftest_web = """
import pytest
from qrunner.utils.log import logger
from qrunner.core.web.driver import Driver

# 用例的前置和后置操作
@pytest.fixture(scope='function', autouse=True)
def init_case():
    # 启动应用
    logger.info('用例开始: 初始化driver')
    driver = Driver()
    yield driver
    # 截图
    logger.info('用例结束: 进行截图')
    driver.allure_shot('用例结束')
    # 停止应用
    logger.info('用例结束: 关闭浏览器')
    driver.close()
"""

    demo_page_adr = """
from qrunner.core.android.element import Element


class HomePage:
    bottom_peer = Element(resourceId='com.qizhidao.clientapp:id/icon2')
    
    def go_peer(self):
        self.bottom_peer.click()
"""
    demo_page_ios = """
from qrunner.core.ios.element import Element


class HomePage:
    bottom_peer = Element(name='查同行', index=2)
    
    def go_peer(self):
        self.bottom_peer.click()
"""
    demo_page_h5 = """
from qrunner.core.h5.element import Element
from selenium.webdriver.common.by import By
from qrunner.core.android.element import Element


class HomePage:
    bottom_peer = Element(resourceId='com.qizhidao.clientapp:id/icon2')
    patent_search = Element(rid='com.qizhidao.clientapp:id/iv_icon', index=1)

    def go_peer(self):
        self.bottom_peer.click()

    def go_patent(self):
        self.patent_search.click()


class PatentPage:
    def __init__(self, d):
        self.d = d
        self.search_input = Element(d, By.CLASS_NAME, 'h-b-content')
    
    def go_search(self):
        self.search_input.click()
"""

    demo_page_web = """
from qrunner.core.web.element import Element
from selenium.webdriver.common.by import By


class PatentPage:
    def __init__(self, d):
        self.d = d
        self.url = 'https://patents-pre.qizhidao.com/'
        self.search_input = Element(d, By.ID, 'driver-home-step1')
    
    def open_page(self):
        self.d.get(self.url)

    def go_search(self):
        self.search_input.click()
"""

    demo_case_android = """
import allure
from pages.android.demo_page import HomePage


@allure.feature('首页信息流')
class TestPeerSearch:
    @allure.title('从首页信息流进入查同行')
    def test(self):
        HomePage().go_peer()
"""

    demo_case_ios = """
import allure
from pages.ios.demo_page import HomePage


@allure.feature('首页信息流')
class TestPeerSearch:
    @allure.title('从首页信息流进入查同行')
    def test(self):
        HomePage().go_peer()
"""

    demo_case_h5 = """
import allure
from qrunner.core.h5.driver import Driver
from pages.h5.demo_page import HomePage, PatentPage


@allure.feature('查专利')
class TestPeerSearch:
    def setup_method(self):
        self.d = Driver()
        self.home_page = HomePage()
        self.patent_page = PatentPage(self.d)

    @allure.title('点击顶部搜索框')
    def test(self):
        self.home_page.go_patent()
        self.patent_page.go_search()
"""
    demo_case_web = """
import allure
from pages.web.demo_page import PatentPage


@allure.feature('首页信息流')
class TestPeerSearch:
    @allure.title('从首页信息流进入查同行')
    def test(self, driver):
        self.patent_page = PatentPage(driver)
        self.patent_page.open_page()
        self.patent_page.go_search()
"""

    demo_require = """
qrunner
"""
    demo_config = """
[device]
serial_no = 
[app]
need_install = no
pkg_name = 
pkg_url = 
"""
    config_handle = """
import os
import configparser
local_path = os.path.dirname(os.path.realpath(__file__))
class Config:
    def __init__(self):
        self.conf_file_path = os.path.join(local_path, 'config.ini')
        self.cf = configparser.ConfigParser()
        self.cf.read(self.conf_file_path, encoding='utf-8')
    def get_name(self, module, key):
        if not self.cf.has_option(module, key):
            print('未找到该数据')
            value = None
        else:
            value = self.cf.get(module, key)
        return value
    def set_name(self, module, key, value):
        if not self.cf.has_section(module):
            self.cf.add_section(module)
        self.cf.set(module, key, value)
        with open(self.conf_file_path, 'w') as f:
            self.cf.write(f)
# 初始化
conf = Config()
"""
    demo_ignore = "\n".join(
        ["allure-results/*", "__pycache__/*", "*.pyc", "report.html", ".idea/*"]
    )

    create_folder(project_name)
    create_folder(os.path.join(project_name, "tests"))
    create_folder(os.path.join(project_name, "tests", "android"))
    create_folder(os.path.join(project_name, "tests", "h5"))
    create_folder(os.path.join(project_name, "tests", "web"))
    create_folder(os.path.join(project_name, "tests", "ios"))
    create_folder(os.path.join(project_name, "pages"))
    create_folder(os.path.join(project_name, "pages", 'android'))
    create_folder(os.path.join(project_name, "pages", 'h5'))
    create_folder(os.path.join(project_name, "pages", 'web'))
    create_folder(os.path.join(project_name, "pages", "ios"))
    create_folder(os.path.join(project_name, "conf"))

    create_file(
        os.path.join(project_name, "tests", "android", "conftest.py"),
        demo_conftest_adr,
    )
    create_file(
        os.path.join(project_name, "tests", "h5", "conftest.py"),
        demo_conftest_adr,
    )
    create_file(
        os.path.join(project_name, "tests", "web", "conftest.py"),
        demo_conftest_web,
    )
    create_file(
        os.path.join(project_name, "tests", "ios", "conftest.py"),
        demo_conftest_ios,
    )
    create_file(
        os.path.join(project_name, "tests", "android", "test_demo.py"),
        demo_case_android,
    )
    create_file(
        os.path.join(project_name, "tests", "h5", "test_demo.py"),
        demo_case_h5,
    )
    create_file(
        os.path.join(project_name, "tests", "web", "test_demo.py"),
        demo_case_web,
    )
    create_file(
        os.path.join(project_name, "tests", "ios", "test_demo.py"),
        demo_case_ios,
    )
    create_file(
        os.path.join(project_name, "pages", "android", "demo_page.py"),
        demo_page_adr,
    )
    create_file(
        os.path.join(project_name, "pages", "h5", "demo_page.py"),
        demo_page_h5,
    )
    create_file(
        os.path.join(project_name, "pages", "web", "demo_page.py"),
        demo_page_web,
    )
    create_file(
        os.path.join(project_name, "pages", "ios", "demo_page.py"),
        demo_page_ios,
    )
    create_file(
        os.path.join(project_name, "conf", "config.ini"),
        demo_config,
    )
    create_file(
        os.path.join(project_name, "conf", "config.py"),
        config_handle,
    )
    create_file(
        os.path.join(project_name, "run.py"),
        demo_run,
    )
    create_file(
        os.path.join(project_name, ".gitignore"),
        demo_ignore,
    )
    create_file(
        os.path.join(project_name, "requirements.txt"),
        demo_require,
    )

    # show_tree(project_name)
    return 0


def main_scaffold(args):
    sys.exit(create_scaffold(args.project_name))

