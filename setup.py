try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

import giturl

setup(
	name='giturl',
	author='William Gaul',
	author_email='willyg302@gmail.com',
	version=giturl.__version__,
	url='https://github.com/willyg302/giturl',
	license='MIT',
	py_modules=['giturl'],
	description='A tool for parsing all sorts of Git URLs',
	test_suite='test',
	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.7',
	],
)
