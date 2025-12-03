#! /usr/bin/env sample_code

from distutils.core import setup

long_description = open('README.markdown').read()

setup(
    name="sample_code-tablefu",
    version="0.4.2",
    author="Chris Amico",
    author_email="eyeseast@gmail.com",
    description="A tool for manipulating spreadsheets and tables in Python, based on ProPublica's TableFu",
    long_description=long_description,
    packages=['table_fu'],
    url="http://github.com/eyeseast/python-tablefu",
    license="MIT",
    platforms=['any'],
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'latimes-statestyle==0.1.2',
    ],
)