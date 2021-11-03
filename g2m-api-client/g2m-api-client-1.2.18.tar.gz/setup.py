import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='g2m-api-client',
    version='1.2.18',
    description='G2M Insights API Client',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://g2m.ai",
    author='G2M Team',
    author_email='info@g2m.ai',
    license='Proprietary',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=['g2mclient'],
    install_requires=[
        "scikit-learn",
    ]
)
