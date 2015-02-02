from distutils.core import setup
import os
import glob

setup(
    name = 'pyspecfit',
    url = 'http://justincely.github.io',
    version = '0.0.1',
    description = 'interact with IRAF task specfit I/O products',
    author = 'Justin Ely',
    author_email = 'ely@stsci.edu',
    keywords = ['astronomy'],
    classifiers = ['Programming Language :: Python',
                   'Development Status :: 1 - Planning',
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering :: Astronomy',
                   'Topic :: Scientific/Engineering :: Physics',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
    packages = ['pyspecfit']
    )
