import setuptools

with open('README.md', 'r') as fh:
	long_description = fh.read()

setuptools.setup(
	name = 'list_tools',
	packages = ['list_tools'],
	version = '0.0.1',
	license='MIT',
	description = 'various list helpers. only chunking, atm',
	long_description=long_description,
	long_description_content_type='text/markdown',
	author = 'Edgars Košovojs',
	author_email = 'kosovojs@gmail.com',
	url = 'https://github.com/kosovojs/list_tools',
	keywords = ['lists', 'split', 'chunk', 'helpers'],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
	],
)
