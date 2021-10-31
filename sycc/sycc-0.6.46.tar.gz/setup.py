#2020-2021
from setuptools import setup
import os
import platform
import sys,time
if platform.system() == 'Linux':#
    pass
elif platform.system() == 'Windows':
    pass
else:
    print('不支持该系统')
    time.sleep(10)
    sys.exit()

__author__ = '神秘的·'
__project_start_time__='2020'
__date_end_time__ = '2021/7,2021/8,2021/9,2021/10'
HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, "README.rst")) as rst:
    R= rst.read()
setup(
    name='sycc', 
    py_modules=['sycc','core','__init__','v'],
    version='0.6.46',
    description='三圆计算器,cmd或shell(Terminal)中输入sycc回车开始运行,ps:ycc是原版,sycc是因作者需要而定制版(不推荐下载) ycc-tset版本是ycc和sycc测试上传版本(请勿下载)', # 
    long_description = R,
    classifiers=[
    'Natural Language :: Chinese (Simplified)',
    'Development Status :: 6 - Mature',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Android',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Terminals',
    'Topic :: System :: Shells',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Intended Audience :: Developers',],
    keywords=['ycc','3y','a_3y','Circle','圆','圆柱','圆环','py','Chinese','sycc',
    'python','windows','linux','3','y','yc','yz'],# 关键字
    author=__author__, 
    author_email='lwb29@qq.com', 
    url='http://pypi.org/project/sycc', 
    license='MIT',
    packages=["p","k","e"],
    python_requires='>=3.6',
    install_requires=['colorama'],
    entry_points = {'console_scripts': ['sycc = sycc:main',]},
    #scripts=['v.py'],
    project_urls = {
    'pydroid(python for android仅限中国大陆使用': 'https://wws.lanzoui.com/iK2GFm24t3a',
    'pydroid文件密码python' : 'https://wws.lanzoux.com/iK2GFm24t3a'
    },
    include_package_data=True,
    zip_safe=True,
)