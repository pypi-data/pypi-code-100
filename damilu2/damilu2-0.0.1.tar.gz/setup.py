from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name='damilu2',
    version='0.0.1',
    author='Hopetree',
    author_email='zlwork2014@163.com',
    description='A web tip of Django',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com',
    keywords='damilu',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.5',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
)