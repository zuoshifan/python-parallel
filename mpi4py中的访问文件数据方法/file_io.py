# file_io.py

"""
Demonstrates the usage of Open, Set_atomicity, Set_view, Seek,
Read, Write, Get_position, Close.

Run this with 4 processes like:
$ mpiexec -n 4 python file_io.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

filename = 'temp.txt'
# open the file, create it if it does not exist
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

# set to be atomicity mode to avoid read/write conflict
fh.Set_atomicity(True)

# set file view, use MPI.INT as etype and filetype
fh.Set_view(0, MPI.INT, MPI.INT)

num_ints = 10 # number of int types
buf1 = np.arange(num_ints, dtype='i')
buf2 = np.zeros(num_ints, dtype='i') # initialize to all zeros

# set individual file pointer of each process
fh.Seek(rank*num_ints, whence=MPI.SEEK_SET)

# each process writes buf1 to file
fh.Write(buf1)

# reset individual file pointer of each process
fh.Seek(rank*num_ints, whence=MPI.SEEK_SET)

# each process reads data to buf2 from file
fh.Read(buf2)

print 'process %d has buf2 = %s' % (rank, buf2)

# check position of individual file pointer
print 'process %d has file pointer position %d after read' % (rank, fh.Get_position())

# close the file
fh.Close()