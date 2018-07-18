from setuptools import setup
import metadocs


import pypandoc
long_description = pypandoc.convert('README.md', 'rst', format='md')


setup(name='metadocs',
      author='Victor Schmidt',
      author_email='vsch@protonmail.com',
      description='The docs of your docs: manage sphinx documentations with mkdocs',
      include_package_data=True,
      keywords='documentation doc sphinx mkdocs metadocs',
      license='AGPL',
      long_description=long_description,
      packages=['metadocs'],
      scripts=['bin/metadocs'],
      url='https://github.com/entrepreneur-interet-general/metadocs',
      version=metadocs.__version__,
      zip_safe=False,
      install_requires=[
          'watchdog',
          'sphinx>=1.7.6',
          'mkdocs',
          'sphinx_rtd_theme>=0.4.0',
          'mkdocs-material',
          'pexpect',
          'pygments'
      ],
      )
