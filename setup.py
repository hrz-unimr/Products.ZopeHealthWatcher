# -*- coding: utf8 -*-
import os
from setuptools import setup, find_packages

README = os.path.join(os.path.dirname(__file__),
                      'README.txt')

setup(name='ZopeHealthWatcher',
      version='0.2',
      description='Monitors A Zope server.',
      long_description=open(README).read(),
      author='Tarek Ziade',
      author_email='tarek@ziade.org',
      url='http://bitbucket.org/tarek/zopewatcher',
      packages=find_packages(),
      namespace_packages=['Products'],
      install_requires=[
          'setuptools',
          'threadframe',
          'Mako'
      ],
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      tests_require=['Nose'],
      test_suite='nose.collector',
      entry_points = {
         "console_scripts": [
            "zope_health_watcher = Products.ZopeHealthWatcher.check_zope:main",
          ]}
      )

