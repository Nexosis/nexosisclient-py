import os
from setuptools import find_packages, setup

with open('README.md') as f:
    long_description = f.read()

build_number = os.getenv('TRAVIS_BUILD_NUMBER', '1')

setup(name='nexosisapi',
      version='2.1.' + build_number,
      description='Python Client for the Nexosis API',
      long_description='This software is provided as a way to include Nexosis API functionality in your own Python '
                       'software. You can read about the Nexosis API at https://developers.nexosis.com',
      url='http://github.com/nexosis/nexosisclient-py',
      author='Nexosis',
      author_email='support@nexosis.com',
      license='Apache 2.0',
      packages=find_packages(),
      install_requires=[
          'requests', 'enum34', 'python-dateutil'
      ],
      test_suite='nexosisapi.tests.all',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      include_package_data=True,
      zip_safe=False)
