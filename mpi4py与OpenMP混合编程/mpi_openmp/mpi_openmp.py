# mpi_openmp.py

"""
Demonstrates how to use mpi4py and OpenMP hybrid programming.

2un this with 2 processes like:
$ mpiexec -n 2 python mpi_openmp.py
"""


from mpi4py import MPI
import hello


comm = MPI.COMM_WORLD

hello.say_hello(comm)