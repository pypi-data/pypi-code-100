from setuptools import setup, find_packages
setup(name='mminepy', # 패키지 명
version='1.6.6',

description='minepy from elbert06',

author='elbert06',

author_email='elbert06@hanmail.net',

license='MIT', # MIT에서 정한 표준 라이센스 따른다
packages=find_packages(),
py_modules=['mminepy'], # 패키지에 포함되는 모듈
python_requires='>=3',
include_package_data=True,
entry_points={
    'console_scripts': [
        'setup = mminepy.hello:gegus',
        'hello = mminepy.hello:gegus',
    ],
},
)