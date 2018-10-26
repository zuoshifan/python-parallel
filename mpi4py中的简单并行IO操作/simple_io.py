# simple_io.py

"""
Demonstrates the usage of individual file pointer and explicit offsets I/O methods.

Run this with 4 processes like:
$ mpiexec -n 4 python simple_io.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank < 3:
    num_ints = 10 # number of int types
else:
    num_ints = 8 # number of int types
buf1 = np.arange(num_ints, dtype='i')
buf2 = np.zeros(10, dtype='i') # initialize to all zeros

offset = 10 * MPI.INT.Get_size() # in unit of bytes

filename = 'temp.txt'

# use individual file pointer
# ------------------------------------------------------------------------------
# open the file for write only, create it if it does not exist
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_WRONLY)

# set individual file pointer of each process
# here we use the default file view, so offset is in bytes
fh.Seek(rank*offset, whence=MPI.SEEK_SET)

# each process writes buf1 to file
fh.Write(buf1)

# close the file
fh.Close()

# open the existed file for read only
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_RDONLY)

print 'size of file: %d bytes' % fh.Get_size()

# set individual file pointer of each process, prepare for reading
fh.Seek(rank*offset, whence=MPI.SEEK_SET)

# each process reads data to buf2 from file
status = MPI.Status()
fh.Read(buf2, status)

# get the amount of data actually read
print 'rank %d read %d MPI.INTs' % (rank, status.Get_count(datatype=MPI.INT))

print 'process %d has buf2 = %s' % (rank, buf2)

# check position of individual file pointer
print 'process %d has file pointer position %d after read' % (rank, fh.Get_position())

# close the file
fh.Close()

# delete the file
if rank == 0:
    MPI.File.Delete(filename)


# use explicit offsets
# ------------------------------------------------------------------------------
# open the file for write only, create it if it does not exist
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_WRONLY)

# each process writes buf1 to file, start from the position of rank*offset
fh.Write_at(rank*offset, buf1)

# close the file
fh.Close()

# open the existed file for read only, and delete the file on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_RDONLY | MPI.MODE_DELETE_ON_CLOSE)

# each process reads data to buf2 from file, start from the position of rank*offset
status = MPI.Status()
fh.Read_at(rank*offset, buf2, status)

# close the file
fh.Close()
