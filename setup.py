# -*- coding: utf-8 -*-
"""Installer for the collective.clamav package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])

tests_require = [
    'plone.app.testing',
    'plone.app.contenttypes',
    'plone.app.robotframework[debug]',
]

setup(
    name='collective.clamav',
    version='2.0a3.dev0',
    description="A product providing clamav antivirus integration for Plone AT and Dexterity content types",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Andreas Mantke',
    author_email='maand@gmx.de',
    url='https://pypi.python.org/pypi/collective.clamav',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'clamd',
        'Plone',
        'archetypes.schemaextender',
        'plone.api',
        'Products.GenericSetup',
        'setuptools',
        'z3c.jbot',
        'plone.app.registry',
    ],
    extras_require={
        'test': tests_require,
        'tests': tests_require,
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
