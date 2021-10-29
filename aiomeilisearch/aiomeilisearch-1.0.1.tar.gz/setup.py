import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiomeilisearch",
    version="1.0.1",
    author="ziyoubaba",
    author_email="1258843771@qq.com",
    description="The MeiliSearch API asyncio client for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ziyoubaba/aiomeilisearch",
    packages=setuptools.find_packages(),
    install_requires=['aiohttp'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)