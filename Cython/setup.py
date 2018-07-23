from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
  ext_modules=cythonize("ArgonSinulatorCython.pyx"),
  include_dir=[numpy.get_include()]
)
