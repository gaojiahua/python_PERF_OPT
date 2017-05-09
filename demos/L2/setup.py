from distutils.core import setup
from Cython.Build import cythonize
setup(name = 'Cpython_test app',
      ext_modules = cythonize("pypy_test.py"))