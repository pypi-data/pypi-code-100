try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='nicrypt',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    version='0.0.3',
    description='A package for encrypting simple texts',
    license='MIT',
    author='Nicolus Rotich',
    author_email='nicholas.rotich@gmail.com',
    install_requires=[
    	"setuptools>=57",
    	"wheel",
    	"cryptography>=35.0.0",
        "fire"
    ],
    url='https://nkrtech.com',
    download_url='https://github.com/moinonin/nicrypt/archive/refs/heads/main.zip',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
)
