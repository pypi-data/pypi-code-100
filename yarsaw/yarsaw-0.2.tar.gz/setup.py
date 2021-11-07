from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = "yarsaw",
    version = "0.2",
    author = "Bruce",
    author_email = "brucealt69@gmail.com",
    description = ("An async wrapper for the Random Stuff API"),
    license = "MIT",
    keywords = "random-stuff-api rsa yarsaw prsaw randomstuff ai-chatbot covid weather jokes",
    packages=['yarsaw'],
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'aiohttp',
    ],
    long_description_content_type= 'text/markdown',
)