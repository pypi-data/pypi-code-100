from setuptools import setup

setup(
	name='mytelegraph',
	author='me',
	description='a tiny helper for posting to a Telegra.ph page.',
	version='0.0.1', 
	packages=['telegraph'], 
	scripts=['bin/posting']
)