from setuptools import setup, find_packages

DESCRIPTION = 'Multi Time Series Encoders'

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="mtse",
    version='0.1.3',
    author="FractalySyn (Corentin Lobet)",
    author_email="<corentin.lobet@etu.unistra.fr>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['torch>=1.7', 'numpy>=1.19', 'pandas>=1.3', 'matplotlib>=3.4'],
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    license='Apache 2.0',
    url="https://github.com/FractalySyn/mtse",
    python_requires=">=3.7",
    include_package_data=True,
    package_data={'': ['data/*']}
)


