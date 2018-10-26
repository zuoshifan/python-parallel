# array_io.py

"""
Demonstrates the usage of nonblocking I/O.

Run this with 6 processes like:
$ mpiexec -n 6 python array_io.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# create a p x q Cartesian process grid
p, q = 2, 3
cart_comm = comm.Create_cart([p, q])
# get the row and column coordinate of each process in the process grid
ri, ci = cart_comm.Get_coords(rank)

# the global array
m, n = 10, 12
global_ary = np.arange(m*n, dtype='i').reshape(m, n)
rs, re = (m/p)*ri, (m/p)*(ri+1) # start and end of row
cs, ce = (n/q)*ci, (n/q)*(ci+1) # start and end of column
# local array of each process
local_ary = np.ascontiguousarray(global_ary[rs:re, cs:ce])
print 'rank %d has local_ary with shape %s' % (rank, local_ary.shape)

filename = 'temp.txt'

# the etype
etype = MPI.INT

# construct filetype
gsizes = [m, n] # global shape of the array
distribs = [MPI.DISTRIBUTE_BLOCK, MPI.DISTRIBUTE_BLOCK] # block distribution in both dimensions
dargs = [MPI.DISTRIBUTE_DFLT_DARG, MPI.DISTRIBUTE_DFLT_DARG] # default distribution args
psizes = [p, q] # process grid in C order
filetype = MPI.INT.Create_darray(p*q, rank, gsizes, distribs, dargs, psizes)
filetype.Commit()

# -------------------------------------------------------------------------------
# use collective I/O or non-collective I/O if collective I/O is not implemented

# open the file for read and write, create it if it does not exist,
# and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

# set the file view
fh.Set_view(0, etype, filetype)

try:
    # collectively write the data to file
    req = fh.Iwrite_all(local_ary)
except NotImplementedError:
    print 'Iwrite_all not implemented, use Iwrite instead'
    # non-collectively write the data to file
    req = fh.Iwrite(local_ary)

# do some computatin or communication here during the nonblocking I/O operation
cnt = 0
while(not req.Test()):
    cnt += 1
print 'rank %d has cnt = %d' % (rank, cnt)

# reset file view
fh.Set_view(0, etype, etype)

# check what's in the file
if rank == 0:
    buf = np.zeros(m * n, dtype='i').reshape(m, n)
    req = fh.Iread_at(0, buf)
    req.Wait()
    assert np.allclose(buf, global_ary)

# close the file
fh.Close()


# -------------------------------------------------------------------------------
# use split collective I/O

# open the file for read and write, create it if it does not exist,
# and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

# set the file view
fh.Set_view(0, etype, filetype)

# begin the split collective write
fh.Write_all_begin(local_ary)

# do some computatin or communication here during the nonblocking I/O operation
for i in range(10):
    pass

# end the split collective write
fh.Write_all_end(local_ary)

# reset file view
fh.Set_view(0, etype, etype)

# check what's in the file
if rank == 0:
    buf = np.zeros(m * n, dtype='i').reshape(m, n)
    req = fh.Iread_at(0, buf)
    req.Wait()
    assert np.allclose(buf, global_ary)

# close the file
fh.Close()
