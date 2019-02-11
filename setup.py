#!/usr/bin/env python
"""setup.py"""
import os
import io
from setuptools import find_packages,setup
import rosette

NAME = "rosette_api"
DESCRIPTION = "Rosette API Python client SDK"
AUTHOR = "Basis Technology Corp."
AUTHOR_EMAIL = "support@rosette.com"
HOMEPAGE = "https://github.com/rosette-api/python"
VERSION = rosette.__version__

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    """read function"""
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as the_file:
            buf.append(the_file.read())
    return sep.join(buf)


LONG_DESCRIPTION = read('README.md')

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      license='Apache License',
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      packages=find_packages(),
      install_requires=['requests'],
      platforms='any',
      url=HOMEPAGE,
      version=VERSION,
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 5 - Production/Stable',
          'Natural Language :: English',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules'])

