#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from spacytei/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("spacytei", "__init__.py")


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='acdh-spacytei',
    version=version,
    description="""A package to ease processing (not only) TEI documents with spaCy""",
    long_description=readme + '\n\n' + history,
    author='Peter Andorfer, Matthias Schlögl, Saranya Balasubramanian',
    author_email='matthias.schloegl@oeaw.ac.at, peter.andorfer@oeaw.ac.at, saranya.balasubramanian@oeaw.ac.at',
    url='https://github.com/acdh-oeaw/acdh-spacytei',
    packages=[
        'spacytei',
    ],
    include_package_data=True,
    install_requires=[
        'spacy>=2.1.4',
        'scikit-learn>=0.20.2',
        'gensim>=3.7.1',
        'lxml>=4.1.1',
        'pandas>=0.23.3',
        'requests>=2.20.1',
        'langid>=1.1.6',
        'jsonschema>=3.0.0',
    ],
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
