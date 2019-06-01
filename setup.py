#!/usr/bin/env python

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name="labpi",
      version=read("VERSION"),
      description="Scripts for reading a chemical barcodes and emptying inventory.",
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      author="Michael Plews",
      author_email="michael.plews@gmail.com",
      url="https://github.com/CabanaLab/LabPi",
      keywords="Raspberry Pi inventory",
      install_requires=[
      ],
      packages=['labpi',],
      entry_points={
          'console_scripts': [
              'run-empty = labpi.empty:main',
          ]
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3.5',
          'Topic :: Scientific/Engineering :: Chemistry',
          'Topic :: Home Automation',
      ]
)
