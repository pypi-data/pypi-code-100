from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='UmbrellaReminder',
    version='0.0.1',
    description='This package contains methods that scrape weather data using Python and sends umbrella reminders to specified email at specified time daily. If the weather condition is rainy or cloudy it will send you an "umbrella reminder" to your email reminding you to pack an umbrella before leaving the house. This package scrapes weather information from Google using bs4 and requests libraries in python. ',
    author= 'Edula Vinay Kumar Reddy',
    url = 'https://github.com/VinayEdula/UmbrellaReminder',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['weather','Reminder','scraping','Rain Reminder', 'Umbrella Reminder','Weather Reminder'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['UmbrellaReminder'],
    package_dir={'':'src'},
    install_requires = [
        'requests',
        'schedule',
        'beautifulsoup4'
    ]
)