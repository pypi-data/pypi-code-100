import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name="parallel_pro",
    version="0.0.1",
    scripts=['parallel_pro/__init__.py'],
    author="Sai Kumar Yava",
    description="parallel_pro is a simple package for parallel processing",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/scionoftech/parallel_pro",
    packages=setuptools.find_packages(),
    keywords=['parallel', 'multi processing'],
    install_requires=["joblib"],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],

)