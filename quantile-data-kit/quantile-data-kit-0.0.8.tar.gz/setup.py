from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quantile-data-kit",
    version="0.0.8",
    author="Jules Huisman",
    author_email="jules.huisman@quantile.nl",
    description="An internal Quantile development kit for making working with data easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quantile-development/quantile-data-kit",
    project_urls={
        "Bug Tracker": "https://github.com/quantile-development/quantile-data-kit/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "dask==2021.9.1",
        "dask-ml==1.9.0",
        "distributed==2021.9.1",
        "pandas==1.3.3",
        "dagster==0.13.0",
        "mlflow==1.20.2",
        "scikit-learn==1.0",
        "yake==0.4.8",
        "boto3==1.18.62",
        "blosc==1.10.6",
        "lz4==3.1.3",
    ],
    extras_require={"test": ["pytest==6.2.5"]},
    packages=find_packages(),
    python_requires=">=3.8",
)
