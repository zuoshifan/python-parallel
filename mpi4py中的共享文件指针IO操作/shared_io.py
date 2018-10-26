# shared_io.py

"""
Demonstrates the usage of I/O with shared file pointers.

Run this with 4 processes like:
$ mpiexec -n 4 python shared_io.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

buf = np.full((5,), rank, dtype='i')

filename = 'temp.txt'

# the etype
etype = MPI.INT
filetype = MPI.INT

# -------------------------------------------------------------------------------
# use blocking non-collective shared file pointer I/O

# open the file for read and write, create it if it does not exist,
# and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

# set the file view
fh.Set_view(0, etype, filetype)

# each process writes buf to file by using blocking non-collective
# shared file pointer write
# there is usually no oreder of the write in this case
print 'rank %d writes %s to file' % (rank, buf)
fh.Write_shared(buf)

# synchronize here to make sure all processes have done the write
comm.barrier()

# reset the shared file pointer
fh.Seek_shared(0)

# check what's in the file
if rank == 0:
    buf1 = np.zeros(5 * size, dtype='i')
    fh.Read_shared(buf1)
    # fh.Read(buf1)
    # fh.Read_at(0, buf1)
    print 'data in the file with Write_shared: %s' % buf1

# close the file
fh.Close()


# # -------------------------------------------------------------------------------
# use blocking collective shared file pointer I/O

# open the file for read and write, create it if it does not exist,
# and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

# set the file view
fh.Set_view(0, etype, filetype)

# each process writes buf to file by using blocking collective
# shared file pointer write
# data will be writen in the order of the rank in this case
print 'rank %d writes %s to file' % (rank, buf)
fh.Write_ordered(buf)

# no need barrier synchronizition when use collective write
# comm.barrier()

# reset the shared file pointer
fh.Seek_shared(0)

# check what's in the file
if rank == 0:
    buf1 = np.zeros(5 * size, dtype='i')
    fh.Read_shared(buf1)
    # fh.Read(buf1)
    # fh.Read_at(0, buf1)
    print 'data in the file with Write_ordered: %s' % buf1

# close the file
fh.Close()

# -------------------------------------------------------------------------------
# use nonblocking split collective shared file pointer I/O

# open the file for read and write, create it if it does not exist,
# and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

# set the file view
fh.Set_view(0, etype, filetype)

# each process writes buf to file by using nonblocking split collective
# shared file pointer write
# data will be writen in the order of the rank in this case
print 'rank %d writes %s to file' % (rank, buf)
fh.Write_ordered_begin(buf)

# can do some computatin/communication here
for i in range(10):
    pass

fh.Write_ordered_end(buf)

# no need barrier synchronizition when use collective write
# comm.barrier()

# reset the shared file pointer
fh.Seek_shared(0)

# check what's in the file
if rank == 0:
    buf1 = np.zeros(5 * size, dtype='i')
    fh.Read_shared(buf1)
    # fh.Read(buf1)
    # fh.Read_at(0, buf1)
    print 'data in the file with Write_ordered_begin and Write_ordered_end: %s' % buf1

# reset the shared file pointer
fh.Seek_shared(0)

# check with Read_ordered_begin and Read_ordered_end
buf2 = np.zeros_like(buf)
fh.Read_ordered_begin(buf2)
fh.Read_ordered_end(buf2)
assert np.allclose(buf, buf2)

# close the file
fh.Close()