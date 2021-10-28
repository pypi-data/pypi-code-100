import random
from setuptools import setup

dependency = random.choice(["Schrodinger", "Cat"])

setup(
    name="paradox",
    version="0.0.2",
    description="A nondeterministic package",
    install_requires=[dependency],
    url="https://dustingram.com/articles/2018/03/05/why-pypi-doesnt-know-dependencies/",
    long_description="<https://dustingram.com/articles/2018/03/05/why-pypi-doesnt-know-dependencies/>",
    long_description_content_type="text/markdown",
)
