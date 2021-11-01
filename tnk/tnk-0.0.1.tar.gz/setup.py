from setuptools import setup

setup(
    name='tnk',
    version='0.0.1',
    description='tensor-numpy-keras',
    url='https://github.com/inagen/tnk',
    author='Timur Bairamokov',
    author_email='inagen57@gmail.com',
    license='BSD 2-clause',
    packages=['tnk'],
    install_requires=['keras',
                      'numpy',
                      'tensorflow==2.6.0',
                      'scipy',
                      'scikit-learn',
                      'pillow',
                      'h5py',
                      'tensorboard~=2.4',
                      'tensorflow-estimator~=2.6',
                      'tensorflow-gpu==2.6.0'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'
    ],
)
