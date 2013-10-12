import os

from setuptools import setup, find_packages

setup(name='friendly-django-topcoat',
      version='1.5.0',
      description='Integrate Adobe\' Topcoat into a Django project',
      long_description='',
      author='ButFriendly',
      author_email='hello@butfriendly.com',
      license='3-Clause BSD',
      url='',
      include_package_data=True,
      classifiers=[],
      namespace_packages=['friendly'],
      packages=find_packages(exclude=['tests']),
      install_requires=['django>=1.5.4'])
