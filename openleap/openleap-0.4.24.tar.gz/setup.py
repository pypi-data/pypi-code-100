from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='openleap', 
    version='0.4.24',
    author='Szymon Ciemała',
    author_email='szymciem@protonmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/szymciem8/OpenLeap",
    description='Hand tracking and gesture recognition module', 
    py_modules=['OpenLeap'], 
    # package_dir={'':'openleap'},
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
    # include_package_data=True,
    package_data={'openleap':['*.pkl']},
    packages=['openleap'],

    license='LICENSE',

    install_requires= [
        "mediapipe ~= 0.8.8",
        "opencv-python ~= 4.5.3.56", 
        "pandas ~= 1.3.4"
    ],    
)