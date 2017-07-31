from codecs import open
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='odswritter',
    version='1.0',

    description='Pandoc`s writter for .ods files.',
    long_description=long_description,

    url='https://github.com/kittypr/PandocOdsWritter',

    author='Julia Zhuk',
    author_email='julettazhuk@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='ods pandoc writter',
    py_modules=['odswritter', 'limages', 'lstyle'],
)
