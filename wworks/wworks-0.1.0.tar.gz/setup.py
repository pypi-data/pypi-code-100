from setuptools import find_packages, setup
from codecs import open

with open("README.md", encoding="utf-8") as f:
    readme_desc = f.read()

setup(
    name="wworks",
    packages=find_packages(include=["wworks"]),
    version="0.1.0",
    url='https://github.com/LMKA/wworks',
    description="a light multiprocessing/multithreading work dispatcher for python.",
    long_description=readme_desc,
    long_description_content_type="text/markdown",
    author="Mehdi LAKBIR",
    author_email="mehdi.lakbir@gmail.com",
    keywords=["python", "light", "multiprocessing", "multithreading", "ProcessPoolExecutor", "ThreadPoolExecutor"],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
    install_requires=["tqdm"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==6.2.5"],
    test_suite="tests",
)