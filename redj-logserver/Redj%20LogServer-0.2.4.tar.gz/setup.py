import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    version='0.2.4',
    author='redj_ai',
    name='Redj LogServer',
    url='https://redj.ai/',
    author_email='info@redj.ai',
    description='Redj Log Server',
    install_requires=['requests'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://redj.ai/",
    },
    classifiers=[
        'Framework :: Django',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires=">=3.6",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)
