import setuptools

setuptools.setup(
    name='ascend_deploy',
    version='1.2',
    packages=setuptools.find_packages(),
    license='',
    author='xisy',
    author_email='thbeh@thbeh.com',
    description='ascend_deploy',
    install_requires=['ascend-io-sdk==0.2.30', 'pyyaml'],
    entry_points={
        'console_scripts': [
            'ascend_download = ascend_deploy.ascend_download:main',
            'ascend_deploy = ascend_deploy.ascend_deploy:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',

)
