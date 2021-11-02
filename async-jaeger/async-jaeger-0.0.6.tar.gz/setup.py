import re

from setuptools import setup, find_packages

version = None
with open('async_jaeger/version.py', 'r') as f:
    for line in f:
        m = re.match(r'^__version__\s*=\s*(["\'])([^"\']+)\1', line)
        if m:
            version = m.group(2)
            break

assert version is not None, \
    'Could not determine version number from async_jaeger/__init__.py'

setup(
    name='async-jaeger',
    version=version,
    url='https://github.com/alvassin/async-jaeger',
    description='Jaeger Python OpenTracing Tracer implementation for AsyncIO',
    author='Alexander Vasin',
    author_email='hi@alvass.in',
    packages=find_packages(exclude=['crossdock', 'tests', 'example', 'tests.*']),
    include_package_data=True,
    license='Apache License 2.0',
    zip_safe=False,
    keywords='jaeger, tracing, opentracing',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
    install_requires=[
        'aiohttp',
        'thriftpy2',
        'opentracing>=2.1,<3.0',
    ],
    # Uncomment below if need to test with unreleased version of opentracing
    # dependency_links=[
    #     'git+ssh://git@github.com/opentracing/opentracing-python.git@BRANCHNAME#egg=opentracing',
    # ],
    test_suite='tests',
    extras_require={
        "dev": [
            "aiomisc",
        ],
        'tests': [
            'mock',
            'pycurl',
            'pytest',
            'pytest-cov',
            'coverage',
            'pytest-timeout',
            'pytest-benchmark[histogram]',
            'pytest-localserver',
            'flake8',
            'flake8-quotes',
            'flake8-typing-imports',
            'codecov',
            'tchannel==2.1.0',
            'opentracing_instrumentation>=3,<4',
            'prometheus_client==0.11.0',
            'mypy',
        ]
    },
)
