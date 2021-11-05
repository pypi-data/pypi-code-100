from setuptools import setup


setup(name='blur_image',
version='0.1.0',
description="""A library to blurring images.""",
long_description="""
# Blur Image
A library to blurring images.
# Install
```
pip3 install blur-image
```
# Using
```python
from blur_image import blur
# blur(source, output, mode = "simple")
# Modes: simple, box, gaussian
# Value is available for this modes: box, gaussian
blur("source.png", "blurred_source.png")
```
""",
long_description_content_type='text/markdown',
url='https://github.com/onuratakan/blur_image',
author='Onur Atakan ULUSOY',
author_email='atadogan06@gmail.com',
license='MIT',
packages=["blur_image"],
package_dir={'':'src'},
install_requires=[
    "Pillow==8.4.0"
],
python_requires=">= 3",
zip_safe=False)