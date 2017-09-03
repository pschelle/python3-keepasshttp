from setuptools import setup, find_packages


setup(name='keepasshttp',
      version='0.2.0',
      description='Python3 port of https://github.com/jobevers/python-keepasshttp',
      author='Markus Freitag',
      author_email='fmarkus@mailbox.org',
      packages=find_packages(exclude=['tests']),
      install_requires=[
          'cryptography',
          'requests'
          ],
      setup_requires=['nose>=1.0'],
      tests_require=['mock==2.0.0']
)
