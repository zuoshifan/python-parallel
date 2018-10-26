# setup.py

import os
# import mpi4py
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

mpi_compile_args = os.popen("mpicc --showme:compile").read().strip().split(' ')
mpi_link_args    = os.popen("mpicc --showme:link").read().strip().split(' ')

ext_modules = [
    Extension(
        "hello",
        ["hello.pyx"],
        # include_dirs = [mpi4py.get_include()],
        extra_compile_args = mpi_compile_args,
        extra_link_args    = mpi_link_args,
    )
]

setup(
    name='hello-parallel-world',
    cmdclass = {"build_ext": build_ext},
    ext_modules = ext_modules
)