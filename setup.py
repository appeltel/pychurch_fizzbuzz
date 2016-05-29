#!/usr/bin/env python

from distutils.core import setup

setup(
    name='PyChurchFizzBuzz',
    version='0.0.1',
    description='FizzBuzz in the Untyped Lambda Calculus',
    author='Eric Appelt',
    author_email='eric.appelt@gmail.com',
    url='https://github.com/appeltel/pychurch_fizzbuzz',
    packages=['fizzbuzz'],
    entry_points={'console_scripts': ['fizzbuzz = fizzbuzz.cli:main']}
)
