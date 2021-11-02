from setuptools import setup, find_packages

EXTRAS_REQUIRE = {
    'dev': (
        'pre-commit',
        'yapf',
        'prospector',
        'pylint',
        'twine',
        'build',
        'pyclean>=2.0.0',  # For cleaning __pycache__ and *.pyc
        'tox',
    ),
    'test': (
        'pytest>=4',
        'pytest-mock',
        'pytest-cases',
    ),
    'doc': ('sphinx', 'sphinx_rtd_theme'),
}

EXTRAS_REQUIRE['full'] = set(value for tup in EXTRAS_REQUIRE.values()
                             for value in tup)

setup(
    packages=find_packages(include=['clease_gui', 'clease_gui.*']),
    extras_require=EXTRAS_REQUIRE,
)
