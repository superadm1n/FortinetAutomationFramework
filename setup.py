#!/usr/bin/env python
from setuptools import setup
from FortinetAutomationFramework import __version__, __author__

description = '''The FortinetAutomationFramework is designed to be an interface for network engineers to 
issue commands and retrieve output from Fortinet Firewalls so they can easily build automation 
scripts atop the framework and dont have to worry about the nuances of CLI scraping.'''

setup(
    name='FortinetAutomationFramework',
    version=__version__,
    packages=['FortinetAutomationFramework'],
    keywords='fortinet automation framework network FortinetAutomationFramework',
    url='https://github.com/superadm1n/FortinetAutomationFramework',
    license='MIT',
    author=__author__,
    author_email='kowalkyl@gmail.com',
    description='Framework for issuing commands and retrieving consistent data on Fortinet devices',
    long_description=description,
    install_requires=['paramiko'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
