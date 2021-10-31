from setuptools import setup
def readme():
    with open('README.md') as f:
        return f.read()
setup(
    name='pricefetch',
    version='0.1.1',
    description='Tool for fetching realtime options and stock data',
    author='Devesh Todarwal, Rutuvi Narang',
    long_description=readme(),
    long_description_content_type= 'text/markdown',
    author_email='todarwal.devesh@gmail.com, rutuvinarang@gmail.com',
    license='MIT',
    packages=['pricefetch'],
    classifiers=[
        'Development Status :: 4 - Beta',  
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Education',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='stocks options finance market shares greeks implied volatility real-time googlefinance yahoofinance',
    install_requires=['requests', 'beautifulsoup4', 'scipy'],
)
