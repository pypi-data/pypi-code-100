from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='KCMiddleware',  # How you named your package folder (MyLib)
    packages=['KCMiddleware'],  # Chose the same as "name"
    version='0.5',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='A Keycloak Middleware',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Alessandro Buffoli',  # Type in your name
    author_email='alessandro.buffoli@evaspa.it',  # Type in your E-Mail
    url='https://gitlab.com/ely-zeus/',  # Provide either the link to your github or to your website
    download_url='https://gitlab.com/ely-zeus/keycloak-middleware-package',  # I explain this later on
    keywords=['KEYCLOAK', 'MIDDLEWARE', 'DJANGO'],  # Keywords that define your package best
    install_requires=[
        'Django >= 3.2.4',
        'python-keycloak >= 0.24.0',
        'djangorestframework >= 3.12.2',
        'PyJWT >= 2.0.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
