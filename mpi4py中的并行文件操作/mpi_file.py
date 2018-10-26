# mpi_file.py

"""
Demonstrates the usage of Open, Set_size, Get_size, Preallocate,
Get_amode, Close, Delete.

Run this with 2 processes like:
$ mpiexec -n 2 python mpi_file.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

filename = 'temp.txt'
# open the file, create it if it does not exist
fh = MPI.File.Open(comm, filename, amode=MPI.MODE_RDWR | MPI.MODE_CREATE)
# set file size to 10 bytes
fh.Set_size(10)
print 'file size: %d bytes' % fh.Get_size()
# preallocate the file to be 20 bytes
fh.Preallocate(20)
print 'file size: %d bytes after preallocate' % fh.Get_size()
# print fh.Get_group()
if fh.Get_amode() == (MPI.MODE_RDWR | MPI.MODE_CREATE):
    print 'amode =  MPI.MODE_RDWR | MPI.MODE_CREATE'
# print fh.Get_info()
# close the file
fh.Close()
# delete the file
if rank == 0:
    MPI.File.Delete(filename)