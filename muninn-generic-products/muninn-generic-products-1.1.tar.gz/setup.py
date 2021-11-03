from setuptools import setup

setup(
    name="muninn-generic-products",
    version="1.1",
    description="Generic Muninn product type extension",
    url="https://github.com/stcorp/muninn-generic-products",
    author="S[&]T",
    license="BSD",
    py_modules=["muninn_generic_products"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Environment :: Plugins",
    ],
    install_requires=["muninn"],
)
