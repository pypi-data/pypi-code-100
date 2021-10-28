"""Setup"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        py_modules=["dekogen_cmd",
                    "dekogen"],
        name="dekogen",
        version="0.1.1",
        author="Denys V. Kondratiuk",
        description="Simple util for generate helper code based on OpenAPI specs",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/denys-ops/dekogen",
        packages=["dekogen"],
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
        ],
        python_requires='>=3.5',
        install_requires=["inflection==0.3.1",
                          "PyYAML==6.0",
                          "Click==7.1.2"],
        entry_points='''
    [console_scripts]
    dekogen_cmd=dekogen_cmd:dekogen_cmd
    ''', )
