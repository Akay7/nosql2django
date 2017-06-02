#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


import os

here = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(here, 'README.md'))
long_description = f.read().strip()
f.close()


setup(
    name='nosql2django',
    version='0.1.1',
    author='Egor Poderiagin',
    author_email='egor@crazyrussian.pro',
    url='https://github.com/Akay7/nosql2django',
    description='Allow convert nosql source to django relational DB structure',
    packages=find_packages(),
    long_description=long_description,
    keywords='django rss atom feeds parser sql nosql-to-sql',
    zip_safe=False,
    install_requires=[
        'Django>=1.8.0',
        'feedparser>=5.2.1',
        'python-dateutil>=2.6.0',
    ],
    test_suite='runtests.runtests',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
