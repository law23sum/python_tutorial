from distutils.core import setup

import numpy
from Cython.Build import cythonize

setup(name='spacy text app',
      ext_modules=cythonize("spacytext.pyx", language="c++"),
      include_dirs=[numpy.get_include()]
      )
