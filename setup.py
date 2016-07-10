#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys
from os import path
from setuptools import setup

def cat(fpath):
    with open(fpath, 'r') as fh:
        blob = fh.read()
        fh.close()
    return blob

desc = 'generate static html5 files from markdown sources (or serve dinamically)'

install_requires = [
    'bottle>=0.12.9',
    'markdown>=2.6.6',
]

setup(
    name = 'bottled-md',
    version = cat('VERSION'),

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
    data_files = [
        ('', ['VERSION']),
        ('templates', [
            'templates/htdoc_head.html',
            'templates/htdoc_tail.html',
        ]),
        ('static', ['static/bmd.css']),
    ],
    zip_safe = False,

    entry_points = {
        'console_scripts': [
            'bmd=bmd:cmd',
        ],
    },
)
