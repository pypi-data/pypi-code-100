# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monochromist', 'monochromist.math_version', 'monochromist.opencv_version']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0',
 'click>=7.1.2,<8.0.0',
 'colour>=0.1.5,<0.2.0',
 'loguru>=0.5.3,<0.6.0',
 'numpy>=1.20.2,<2.0.0',
 'opencv-python>=4.5.1,<5.0.0']

entry_points = \
{'console_scripts': ['monochromist = monochromist.math_version.process:process',
                     'monochromist_opencv = '
                     'monochromist.opencv_version.process:process']}

setup_kwargs = {
    'name': 'monochromist',
    'version': '1.0.1',
    'description': 'Convert your sketch into contour with transparent background',
    'long_description': '# monochromist\n\nFrom sketch to contour with transparent background:\n\n![example](https://github.com/ozzzzz/monochromist/blob/main/doc/images/cat_illustration.png)\n\nMinimum example:\n```bash\nmonochromist -i <input image> -o <output image> -c "<color>"\n```\n\nFor example:\n```bash\nmonochromist -i doc/images/cat.jpg -o /tmp/cat.png -c "black"\n```\n\nFor more settings run\n```bash\nmonochromist --help\n```',
    'author': 'Bogdan Neterebskii',
    'author_email': 'bog2dan1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ozzzzz/monochromist',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
