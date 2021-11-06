from setuptools import setup
setup(
    name="msgs",
    version="1.0.1",
    packages=["msgs"],
    description="networkmsgs",
    author="liuzihao",
    keywords="network msgs app",
    install_requires=[],
    python_requires=">=3",
    entry_points={
        'console_scripts': ['msgs=msgs.networkmsgs:runapp']
    },
    project_urls={
        "Source Code":"https://gitee.com/haozihan/msgs/tree/master/",
    },
)
