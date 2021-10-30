import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='protectonce',
    version='0.0.1',
    author="protectonce",
    author_email="protectonce@protectonce.com",
    description="python agent package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ProtectOnce/python_agent.git",
    install_requires=['wrapt', 'orjson'],
    classifiers=[
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
    package_dir={"": "out"},
    package_data={'': ['./agent_interface/out/libprotectonce.so']},
    packages=setuptools.find_packages(where="out")

)
