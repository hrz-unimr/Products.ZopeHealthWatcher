# -*- coding: utf8 -*-

import os
from setuptools import setup, find_packages

README = os.path.join(os.path.dirname(__file__),
                      'README.rst')

setup(name='Products.ZopeHealthWatcher',
      version='0.5.0',
      description='Monitors A Zope server.',
      long_description=open(README).read(),
      author='Tarek Ziade',
      author_email='tarek@ziade.org',
      maintainer='Alexander Loechel',
      maintainer_email='Alexander.Loechel@lmu.de',
      url='http://github.com/collective/Products.ZopeHealthWatcher',
      license='GPLv2',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['Products'],
      install_requires=[
          'setuptools',
          'Mako'
      ],
      classifiers=[
          'Framework :: Plone',
          'Framework :: Zope2',
          'Framework :: Plone :: 3.3',
          'Framework :: Plone :: 4.0',
          'Framework :: Plone :: 4.1',
          'Framework :: Plone :: 4.2',
          'Framework :: Plone :: 4.3',
          'Framework :: Plone :: 5.0',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Monitoring',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
      ],
      tests_require=['Nose'],
      test_suite='nose.collector',
      include_package_data=True,
      entry_points={
          "console_scripts": [
              "zHealthWatcher = Products.ZopeHealthWatcher.check_zope:main",
          ]}
      )
