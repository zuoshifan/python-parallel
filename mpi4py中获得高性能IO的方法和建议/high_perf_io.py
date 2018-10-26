# high_perf_io.py

"""
Demonstrates the four levels of access.

Run this with 16 processes like:
$ mpiexec -n 16 python high_perf_io.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# create a p x q Cartesian process grid
p, q = 4, 4
cart_comm = comm.Create_cart([p, q])
# get the row and column coordinate of each process in the process grid
ri, ci = cart_comm.Get_coords(rank)

# the global array
lm, ln = 3, 2 # shape of local subarray
m, n = p*lm, q*ln # shape of global array
global_ary = np.arange(m*n, dtype='i').reshape(m, n)
rs, re = lm*ri, lm*(ri+1) # start and end of row
cs, ce = ln*ci, ln*(ci+1) # start and end of column
# local array of each process
local_ary = np.ascontiguousarray(global_ary[rs:re, cs:ce])
print 'rank %d has local_ary with shape %s' % (rank, local_ary.shape)

filename = 'temp.txt'

# the etype
etype = MPI.INT

# construct filetype
gsizes = [m, n] # global shape of the array
subsize = [lm, ln] # shape of local subarray
starts = [rs, cs] # global indices of the first element of the local array
filetype = MPI.INT.Create_subarray(gsizes, subsize, starts)
filetype.Commit()

# first write the global array to a file
if rank == 0:
    fh = MPI.File.Open(MPI.COMM_SELF, filename, amode=MPI.MODE_CREATE | MPI.MODE_WRONLY)
    fh.Write(global_ary)
    fh.Close()

comm.Barrier()


# level 0
# ----------------------------------------------------------------------------------

local_ary1 = np.zeros_like(local_ary)

fh = MPI.File.Open(comm, filename, amode=MPI.MODE_RDONLY)
for i in range(lm):
    offset = etype.Get_size() * ((rs + i) * n + cs)
    fh.Seek(offset)
    # each process uses individual read
    fh.Read(local_ary1[i, :])
    # fh.Read_at(offset, local_ary1[i, :])
assert np.allclose(local_ary, local_ary1)
fh.Close()


# level 1
# ----------------------------------------------------------------------------------

local_ary1 = np.zeros_like(local_ary)

fh = MPI.File.Open(comm, filename, amode=MPI.MODE_RDONLY)
for i in range(lm):
    offset = etype.Get_size() * ((rs + i) * n + cs)
    fh.Seek(offset)
    # use collective read
    fh.Read_all(local_ary1[i, :])
    # fh.Read_at_all(offset, local_ary1[i, :])
assert np.allclose(local_ary, local_ary1)
fh.Close()


# level 2
# ----------------------------------------------------------------------------------

local_ary1 = np.zeros_like(local_ary)

fh = MPI.File.Open(comm, filename, amode=MPI.MODE_RDONLY)
fh.Set_view(0, etype, filetype)
# each process uses individual read
fh.Read(local_ary1)
# fh.Read_at(0, local_ary1)
assert np.allclose(local_ary, local_ary1)
fh.Close()


# level 3
# ----------------------------------------------------------------------------------

local_ary1 = np.zeros_like(local_ary)

fh = MPI.File.Open(comm, filename, amode=MPI.MODE_RDONLY)
fh.Set_view(0, etype, filetype)
# use collective read
fh.Read_all(local_ary1)
# fh.Read_all_all(0, local_ary1)
assert np.allclose(local_ary, local_ary1)
fh.Close()

# remove the file
if rank == 0:
    MPI.File.Delete(filename)
