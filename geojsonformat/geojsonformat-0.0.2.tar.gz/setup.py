import setuptools

with open('README.md', 'r') as fh:
	long_description = fh.read()

setuptools.setup(
	name = 'geojsonformat',
	packages = ['geojsonformat'],
	version = '0.0.2',
	license='MIT',
	description = 'format geojson',
	long_description=long_description,
	long_description_content_type='text/markdown',
	author = 'Edgars Košovojs',
	author_email = 'kosovojs@gmail.com',
	url = 'https://github.com/kosovojs/geojsonformat',
	keywords = ['geojson'],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
	],
	entry_points={
		'console_scripts':
			['geojsonformat = geojsonformat:format']
	}
)
