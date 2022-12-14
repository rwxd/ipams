from setuptools import setup
from os import path

__version__ = "1.1.0"

with open("./requirements.txt") as f:
    required = f.read().splitlines()

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ipams',
    version=__version__,
    description='Tool to query multiple IPAMs.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='rwxd',
    author_email='rwxd@pm.me',
    url="https://github.com/rwxd/ipams",
    license='MIT',
    packages=['ipams'],
    install_requires=required,
    entry_points={"console_scripts": ["ipams = ipams.__main__:main"]},
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
