import os
from glob import glob
from distutils.core import setup
from Cython.Build import cythonize

setup(name='RS API', ext_modules=cythonize("model.pyx", build_dir="build"))

so_file = glob('model.cpython*.so')[0]
lib_name, *_, file_ext = so_file.split('.')
os.rename(so_file, f'{lib_name}.{file_ext}')
