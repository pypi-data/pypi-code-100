from setuptools import setup

long_description = open('README.md').read()
setup(
	version='0.0.5',
	url='https://github.com/aN4ksaL4y/mytelegraph',
	name='mytelegraph',
	author='Muhammad Al Fajri',
	author_email='fajrim228@gmail.com',
	description='a tiny helper for posting to a Telegra.ph page.',
	long_description = long_description,
	long_description_content_type='text/markdown',
	install_requires=['icecream', 'requests', 'faker'],
	packages=['telegraph'], 
	scripts=['bin/posting']
)
