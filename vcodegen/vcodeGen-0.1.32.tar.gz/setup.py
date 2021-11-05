from setuptools import find_packages,setup
from xes import version
setup(
    name = 'vcodeGen',
    version = version.version,
    author = 'Ruoyu Wang',
    description = '轻易地生成图片验证码，防止你的网站被爬虫。',
    packages = find_packages(),
    #install_requires = ["requests", "pypinyin", "pygame"],
    url = 'https://code.xueersi.com'
)