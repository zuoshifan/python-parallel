# noncontig_io.py

"""
Demonstrates the usage of noncontiguous accesses and collective I/O.

Run this with 3 processes like:
$ mpiexec -n 3 python noncontig_io.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

buf1 = np.arange(10, dtype='i')
buf2 = np.zeros(10, dtype='i') # initialize to all zeros

filename = 'temp.txt'

# open the file for read and write, create it if it does not exist,
# and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

# displacement in bytes of each process
disp = (5 + rank * 2) * MPI.INT.Get_size()
# the etype
etype = MPI.INT

# construct filetype, which consists of 2 ints and a gap of 4 ints
INT2 = MPI.INT.Create_contiguous(2)
filetype = INT2.Create_resized(0, 6*MPI.INT.Get_size())
filetype.Commit()

# set the file view, which is a collective operation
fh.Set_view(disp, etype, filetype)

if rank == 0:
    # rank 0 writes buf1 to the file
    # the 10 interges will be writen into noncontiguous positions
    # in the file with a single write call
    fh.Write(buf1)
    # rank 0 reads data from file to buf2
    # 10 interges in noncontiguous positions of the file will be read
    # with a single read call
    fh.Read_at(0, buf2)
    print 'buf2:', buf2

# use collective I/O method
# first reset the individual file pointer to the beginning of the file
fh.Seek(0, whence=MPI.SEEK_SET)

# collectively write the data to file
fh.Write_all(buf1)

# reset the file view for read, which is a collective operation
fh.Set_view(disp, etype, etype)

# check what's in the file
if rank == 0:
    buf3 = np.zeros(30, dtype='i') # initialize to all zeros
    fh.Seek(0, whence=MPI.SEEK_SET)
    fh.Read(buf3)
    print 'buf3:', buf3
    # buf3: [0 1 0 1 0 1 2 3 2 3 2 3 4 5 4 5 4 5 6 7 6 7 6 7 8 9 8 9 8 9]
    # rank 0 ---         ---         ---         ---         ---
    # rank 1     ---         ---         ---         ---         ---
    # rank 2         ---         ---         ---         ---         ---

# close the file
fh.Close()
