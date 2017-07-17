from setuptools import find_packages, setup

with open('README.md') as f:
    long_description = f.read()

setup(name='nexosisapi',
      version='1.0.0',
      description='Python Client for the Nexosis API',
      long_description=long_description,
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
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      include_package_data=True,
      zip_safe=False)
