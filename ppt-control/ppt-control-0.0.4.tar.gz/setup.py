import setuptools
from os import path
import ppt_control      # Import main module so we can set the version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setuptools.setup(
    name='ppt-control',
    version=ppt_control.__version__,
    description='Interface for controlling PowerPoint slideshows over WebSocket/HTTP',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://git.lorimer.id.au/ppt-control.git',
    author='Andrew Lorimer',
    author_email='andrew@lorimer.id.au',
    classifiers=[                       # https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Multimedia'
    ],
    keywords='ppt-control ppt_control powerpoint ppt',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',    # as of v0.0.1, OBS only supports use of Python 3.6 for scripts. Otherwise the package works fine on > 3.6.
    install_requires=['pywin32', 'websockets', 'pystray'],   # https://packaging.python.org/en/latest/requirements.html
    data_files=[(ppt_control.CONFIG_DIR, [ppt_control.CONFIG_FILE])],
    entry_points={'gui_scripts': ['ppt-control = ppt_control.ppt_control:start_interface']},
    package_data={"": ["static/*", "static/icons/*"]}
    #include_package_data=True
)
