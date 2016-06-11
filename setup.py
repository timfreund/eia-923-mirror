from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='eia-923-mirror',
    version='0.1.0',

    description='EIA Form 923 Mirror',
    long_description=long_description,
    url='https://github.com/timfreund/eia-923-mirror',
    author='Tim Freund',
    author_email='tim@freunds.net',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords='opendata government',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[],

    entry_points={
        'console_scripts': [
            'eia-923-mirror=eia923:mirror',
        ],
    },
)
