from setuptools import setup

long_description = open('README.md').read()
setup(
	url='https://github.com/aN4ksaL4y/mytelegraph',
	name='mytelegraph',
	author='Cingkariak Sawah',
	author_email='fajrim228@gmail.com',
	description='a tiny helper for posting to a Telegra.ph page.',
	long_description = long_description,
	long_description_content_type='text/markdown',
	version='0.0.3', 
	packages=['telegraph'], 
	scripts=['bin/posting']
)
