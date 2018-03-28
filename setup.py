#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: setup.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 19.10.2017
from setuptools import find_packages, setup


setup(
    name='chance-soya',
    version="0.0.2",
    description='The python project for calculating financial indexes',
    url='https://github.com/chancefocus/soya',
    author='Jimin Huang',
    author_email='huangjimin@whu.edu.cn',
    license='MIT',
    packages=find_packages(exclude='tests'),
    install_requires=[
        'arrow>=0.7.0',
        'mock>=2.0.0',
        'nose>=1.3.7',
        'coverage>=4.1',
        'Sphinx>=1.6.5',
        'sphinx-rtd-theme>=0.1.9'
        'chance-config>=0.0.4',
        'pandas==0.22.0',
    ],
    package_data={
        '': ['*.yaml', ],
    },
)
