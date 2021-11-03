import setuptools

setuptools.setup(
    name='GladSpamBot',
    version='0.0.61',
    description='Module to log into 20 bots with bot token no memory lock issue!',
    long_description="Module to log into 20 bots without any memory lock...",
    author='Gladiators-Projects',
    author_email='gladiatorsprojects@gmail.com',
    url = 'https://github.com/Gladiators-Projects',
    install_requires=["heroku3==5.1.4", "telethon==1.23.0", "gitpython==3.1.18", "python-decouple==3.4", "sqlalchemy==1.3.20", "cryptg", "psycopg2==2.9.1"],
    packages=setuptools.find_packages(),
    keywords=['Gladiators', 'SpamBot', 'spammerbots', 'GladSpamBot', 'Gladiators-Projects', 'SpamBot'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",  
    ],
)