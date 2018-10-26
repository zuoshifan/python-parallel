# cython_mpi.py

"""
Demonstrates how to use mpi4py in cython.

Run this with 4 processes like:
$ mpiexec -n 4 python cython_mpi.py
"""

from mpi4py import MPI
import hello


comm = MPI.COMM_WORLD


hello.say_hello(comm)
hello.c_say_hello(comm)

new_comm = hello.return_comm(comm)

if not new_comm is None:
    print 'new_comm.size = %d' % new_comm.size