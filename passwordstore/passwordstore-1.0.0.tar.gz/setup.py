from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='passwordstore',
    version='1.0.0',
    author="MaksL",
    author_email="contactmaksloboda@gmail.com",
    description=u"Small utility to generate secure passwords from masterpass word",
    long_description_content_type="text/markdown",
    url="https://github.com/maksloboda/PasswordStore",
    project_urls={
        "Bug Tracker": "https://github.com/maksloboda/PasswordStore/issues",
    },
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=['main'],
    install_requires=[
        'click',
        'cryptography',
        'pyperclip',
    ],
    entry_points={
        'console_scripts': [
            'passwordstore = main:cli',
        ],
    },
    python_requires=">=3.6",
)
