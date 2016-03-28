#!/usr/bin/env python
from setuptools import setup
import rosette
import os
import io

NAME = "rosette_api"
DESCRIPTION = "Rosette API Python client SDK"
AUTHOR = "Basis Technology Corp."
AUTHOR_EMAIL = "rosette_api@basistech.com"
HOMEPAGE = "https://developer.rosette.com"
VERSION = rosette.__version__

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      license='Apache License',
      long_description=long_description,
      packages=['rosette'],
      install_requires=['requests'],
      platforms='any',
      url=HOMEPAGE,
      version=VERSION,
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 4 - Beta',
          'Natural Language :: English',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules']
      )
