from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pandocodswriter',
    version='1.0',

    description='Pandoc`s writer for .ods files.',
    long_description=long_description,

    url='https://github.com/kittypr/PandocOdsWriter',

    author='Julia Zhuk',
    author_email='julettazhuk@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='ods pandoc writer',

    install_requires=['odfpy==1.3.5'],

    scripts=['pandocodswriter/odswriter.py'],

    packages=find_packages()
)
