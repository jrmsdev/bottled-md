#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys
from os import path
from setuptools import setup, find_packages

desc = 'generate static html5 files from markdown sources (or serve dinamically)'

install_requires = [
    'bottle>=0.12.9',
    'markdown>=2.6.6',
]

setup(
    name = 'bottled-md',
    version = 'v17.6.1',

    description = desc,
    long_description = desc,

    license = 'BSD',
    url = 'https://github.com/jrmsdev/bottled-md',

    author = 'Jeremías Casteglione',
    author_email = 'git@jrms.com.ar',

    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
    ],

    install_requires = install_requires,

    py_modules = ['bmd', 'mdx'],
    data_files = [('', ['htdoc_head.html', 'htdoc_tail.html'])],
    zip_safe = False,

    entry_points = {
        'console_scripts': [
            'bmd=bmd:cmd',
        ],
    },
)
