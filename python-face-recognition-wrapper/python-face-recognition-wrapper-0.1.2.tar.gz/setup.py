import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='python-face-recognition-wrapper',
    version='0.1.2',
    author='Smirnov.EV',
    author_email='knyazz@gmail.com',
    description='wrapper of face recognition sdk to compare faces',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/knyazz/face-recognition',
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta'
    ],
    install_requires=[
        'numpy==1.21.3',
        'Pillow==8.4.0',
        'face_recognition_models==0.3.0',
        'face-recognition==1.3.0',
        'dlib==19.22.1',
        'click==8.0.3',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)
