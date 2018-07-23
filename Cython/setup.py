from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
  ext_modules=cythonize("ArgonSimulatorCython.pyx"),
  include_dir=[numpy.get_include()]
)
