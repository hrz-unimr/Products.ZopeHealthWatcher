# -*- coding: utf8 -*-
import os
from setuptools import setup, find_packages

README = os.path.join(os.path.dirname(__file__),
                      'README.txt')

setup(name='ZopeHealthWatcher',
      version='0.1',
      description='Monitor A Zope installation',
      long_description=open(README).read(),
      author='Tarek Ziade',
      author_email='tarek@ziade.org',
      url='http://bitbucket.org/tarek',
      packages=find_packages(),
      namespace_packages=['Products'],
      install_requires=[
          'setuptools',
      ],
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      entry_points = {
         "console_scripts": [
            "zope_watcher = Products.DeadlockDebugger.check_zope:main",
          ]}
      )

