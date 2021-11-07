import pathlib
from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()


test_requirements = ['pytest>=3', ]

HERE = pathlib.Path(__file__).parent
README = (HERE/"README.md").read_text()

setup(
    author="Zidaan Habib",
    author_email='hbbzid001@myuct.ac.za',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Interacts with a pedestal device as a controller",
    entry_points={
        'console_scripts': [
            'nextrad=nextrad_client.__main__:main',
        ],
    },
    install_requires=["pynmea2",
    "paho-mqtt", "pyserial"
        ],
    license="GNU General Public License v3",
    long_description=README,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='nextrad',
    name='nextrad_client',
    #packages=find_packages(include=['']),
    packages=["nextrad_client"],
    #setup_requires=setup_requirements,
    tests_require=["pytest"],
    url='https://github.com/ZidaanHabib/nextrad-linky-links',
    version='1.0.0',
    zip_safe=False,
)