from setuptools import setup

setup(
        name="fc_mkdxd_bigdata",#项目名   包名
        version = "1.0",    #版本号
        py_modules=["fc_mkdpy_bigdata"],#生成模块     要打包的文件
        author="大数据3",       #作者
        author_email="fc@bigdata.com",#邮箱
        description="毛坤铎"    #项目信息   对包名进行的描述
)

# pip install wheel
# pip install twine
#python setup.py sdist
#python setup.py bdist_wheel
#twine upload dist/*
#安装自己上传的包
# pip install fc-digdata3 -i https://pypi.org/simple/