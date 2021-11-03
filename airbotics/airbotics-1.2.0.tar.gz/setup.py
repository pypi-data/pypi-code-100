from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='airbotics',
    version='1.2.0',
    license='Apache-2.0',
    maintainer='AndrewAirbotics',
    maintainer_email='hello@airbotics.io',
    description='Python SDK for Airbotics',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='robotics, ros, ros2, slam',
    project_urls={
        'Source': 'https://github.com/Airbotics/python-sdk',
        'Tracker': 'https://github.com/Airbotics/python-sdk/issues'
    },
    packages=['airbotics'],
    python_requires='>=3.8',
    install_requires=[
        'requests==2.25.1',
        'numpy==1.21.0',
        'Pillow==8.3.1'
    ],
)