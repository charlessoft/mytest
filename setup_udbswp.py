#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<roy@binux.me>
#         http://binux.me
# Created on 2014-11-24 22:27:45


import sys
from setuptools import setup, find_packages
from codecs import open
from os import path

install_requires = [
    'pyspider',
    'requests>=2.2',
    'pymongo>=2.7.2,<3.0',
    'python-dateutil',
    'ujson',
    'redis',
]

extras_require_all = [
]


setup(
    name='udbswp',
    version='0.1',

    description='this is udb spider workplace',
    long_description='this is udb spider workplace',

    author='Mithril',
    author_email='not_exist@not_exist.com',

    license='Private',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',

        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',

        'Topic :: Internet :: WWW/HTTP',
    ],

    keywords='',

    packages=find_packages(include=['udbswp']),

    install_requires=install_requires,

    extras_require={
        'all': extras_require_all,
        'test': [
            'unittest2>=0.5.1',
            'coverage',
        ]
    },

)
