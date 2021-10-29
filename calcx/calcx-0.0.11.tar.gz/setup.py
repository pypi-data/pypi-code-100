from setuptools import setup, find_packages

setup(
    name='calcx',
    version='0.0.11',
    description='Calculate the indicators of fund',
    author='ZD',
    author_email='995084571@qq.com',
    py_modules=["calcx"],
    packages=['calcx'],
    license='MIT',
    platform='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    install_requires=['pandas', 'numpy']
)