#setup.py
from distutils.core import setup, Extension
setup(name='example',
      version='1.0.0',
      description='Simple SWIG example ',
      ext_modules=[Extension('_example', sources=['example.c', 'example.i'])]
      )