# io_interop.py

"""
Demonstrates how to write portable files.

Run this with 2 processes like:
$ mpiexec -n 2 python io_interop.py
"""


import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# buf1 =
# buf2 = bytearray([0]*100)

filename = 'temp.txt'

def extent_fn(dtype):
    print 'dtype: %s' % dtype
    return 4

print MPI.Register_datarep('rep', None, None, extent_fn)
# print MPI.Register_datarep('native', None, None, extent_fn)

# open the file for read and write, create it if it does not exist,
# and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

etype = MPI.INT
filetype = MPI.INT

# set the file view
# fh.Set_view(0, etype, filetype, 'rep')
fh.Set_view(0, etype, filetype, 'external32')

# close the file
fh.Close()

print 'done'