from setuptools import setup, find_packages

setup(
  name="GML Analyzer",
  version="0.0.1",
  description="A library for analyzing and indexing Graffiti Markup Language tags",
  author="Golan Levin",
  author_email="golan@flong.com",
  packages=find_packages(),
  test_suite='nose.collector',
  tests_require=['nose']
)