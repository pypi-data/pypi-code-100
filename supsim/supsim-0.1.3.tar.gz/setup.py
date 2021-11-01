import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    readme = fh.read()

with open("requirements.txt", encoding="utf-8") as r:
    requirements = [i.strip() for i in r]

setuptools.setup(
    name='supsim',
    version='0.1.3',
    author='Morteza Nazifi and Hamid Fadishei',
    author_email='fadishei@yahoo.com',
    description='A software developed for studying two-predictor suppressor effects via computerized simulations',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://supsim.netlify.app',
    license='GPLv3+',
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['supsim = supsim.supsim:main']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords='regression,suppression',
    python_requires='>=3.6',
    install_requires=requirements,
)
