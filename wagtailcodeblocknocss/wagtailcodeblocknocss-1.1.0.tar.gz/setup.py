from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="wagtailcodeblocknocss",
    description="Slightly modified wagtailcodeblock for custom PrismJS themes.",
    version='1.1.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Averyanov Oleg",
    author_email="lego5621@gmail.com",
    url="https://github.com/lego5621/wagtailcodeblocknocss",
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=["wagtail>=2.13",],
    setup_requires=["setuptools_scm"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
