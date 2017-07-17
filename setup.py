from setuptools import setup

setup(name='nexosisclient',
      version='1.0',
      description='Python Client for the Nexosis API',
      url='http://github.com/nexosis/nexosisclient-py',
      author='Nexosis',
      author_email='support@nexosis.com',
      license='Apache 2.0',
      packages=['nexosisclient'],
      install_requires=[
          'requests', 'enum34', 'python-dateutil'
      ],
      test_suite='nexosisclient.test.all',
      classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
      ),
      zip_safe=False)
