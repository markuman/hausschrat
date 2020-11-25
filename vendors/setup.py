from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='hausschrat_nextcloud_s3',
      version='1',
      description='hausschrat mixed vendor example',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://git.osuv.de/m/hausschrat',
      author='Markus Bergholz',
      author_email='git@osuv.de  ',
      license='WTFPL',
      packages=['hausschrat_nextcloud_s3'],
      zip_safe=True)
