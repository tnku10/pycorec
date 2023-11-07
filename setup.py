#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ['customtkinter>=5.2.0', 'packaging>=23.2', 'Pillow>=10.0.0', 'natsort>=8.4.0',
                'openpyxl>=3.1.2', 'screeninfo~=0.8.1']

test_requirements = []

setup(
    author="Yuto Tanaka",
    author_email='tanaka.yuto.u10@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',

    ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    entry_points={
        'console_scripts': [
            'pycorec=pycorec.pycorec:main',
        ],
    },
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords='pycorec',
    name='pycorec',
    packages=find_packages(include=['pycorec', 'pycorec.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tnku10/pycorec',
    version='2.0.6',
    zip_safe=False,
)
