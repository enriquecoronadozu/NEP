import os, re; from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme: README = readme.read()
with open(os.path.join(os.path.dirname(__file__), 'pysettings','__init__.py')) as fd:
	__version__ = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

setup(
	name='pysettings',
	version=__version__,
	packages=find_packages(),
	include_package_data=True,
	license='MIT License',
	description='Python library to provide settings files for modular applications',
	long_description=README,
	url='https://github.com/UmSenhorQualquer/pysettings',
	author='Ricardo Jorge Vieira Ribeiro',
	author_email='ricardojvr@gmail.com',
	classifiers=[
		'Intended Audience :: Developers',
		'License :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
	],
)