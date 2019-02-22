#!/usr/bin/env python
# -*- coding: utf-8 -*-

version = "0.0.4"

try:
    import fastentrypoints
except ImportError:
    from setuptools.command import easy_install
    import pkg_resources
    easy_install.main(['fastentrypoints'])
    pkg_resources.require('fastentrypoints')
    import fastentrypoints

import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info[0] == 2:
    jsonrpclib = "jsonrpclib"
elif sys.version_info[0] == 3:
    jsonrpclib = "jsonrpclib-pelix"

setup(
    name='zerophone',
    py_modules=['zerophone'],
    version=version,
    description='ZeroPhone API library, with CLI',
    author='CRImier',
    author_email='crimier@yandex.ru',
    install_requires=[
        jsonrpclib
    ],
    url = 'https://github.com/ZeroPhone/Zerophone-API-Python',
    download_url = 'https://github.com/ZeroPhone/zerophone-api-py/archive/{}.tar.gz'.format(version),
    entry_points={"console_scripts": ["zp = zerophone:main"]},
)
