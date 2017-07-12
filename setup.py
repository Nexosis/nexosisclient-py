from setuptools import setup

setup(name='nexosisclient',
      version='1.0',
      description='Python Client for the Nexosis API',
      url='http://github.com/nexosis/nexosisclient-py',
      author='Nexosis',
      license='Apache2',
      packages=['nexosisclient'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
