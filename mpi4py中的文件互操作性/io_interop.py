# io_interop.py

"""
Demonstrates how to write portable files.
File created in this way can be read with any MPI implementation on any machine.

Run this with 2 processes like:
$ mpiexec -n 2 python io_interop.py
"""


import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

filename = 'temp.txt'

# open the file for read and write, create it if it does not exist,
# and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

# this just sets the data representation to external32 (with dummy values
# for disoplacement, etype and filetype)
fh.Set_view(0, MPI.BYTE, MPI.BYTE, 'external32')

# get the extent of MPI.INT when data representation is set to external32
extent_in_file = fh.Get_type_extent(MPI.INT)

# construct filetype, which consists of 2 ints and a gap of 4 ints
# instead of using MPI.INT.Get_size(), we use extent_in_file to calculate extent
INT2 = MPI.INT.Create_contiguous(2)
lb = 0
extent = (2 + 4) * extent_in_file
filetype = INT2.Create_resized(lb, extent)
filetype.Commit()

etype = MPI.INT
# the displacement in the file is also calculated by using extent_in_file
disp = 5 * extent_in_file

# set the file view (with the real displacement, etype and filetype)
fh.Set_view(disp, etype, filetype, 'external32')

buf = np.arange(10*rank, 10*(rank+1), dtype='i')

# set the individual file pointer and write data to file
fh.Seek(rank*10, whence=MPI.SEEK_SET)
fh.Write(buf)

# check what's in the file
if rank == 0:
    buf1 = np.zeros(10*comm.size, dtype='i')
    fh.Read_at(0, buf1)
    print 'data in file: %s' % buf1

# close the file
fh.Close()