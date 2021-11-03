from setuptools import setup, find_packages

setup_args = dict(
    name='stannismod_ppp',
    version='0.1',
    description='The test package',
    license='MIT',
    packages=find_packages(),
    url='https://github.com/StannisMod/stannismod_ppp',
    author='Stanislav Batalenkov',
    author_email='stas.batalenkov@mail.ru'
)

install_requires = [
    'numpy',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)