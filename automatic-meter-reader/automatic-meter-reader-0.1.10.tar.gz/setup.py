from setuptools import setup

setup(name="automatic-meter-reader",
    version="0.1.10",
    url="https://github.com/ardiloot/automatic-meter-reader",
    author="Ardi Loot",
    author_email="ardi.loot@outlook.com",
    packages=["automatic_meter_reader"],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "meter-digits-recognizer",
    ]
)