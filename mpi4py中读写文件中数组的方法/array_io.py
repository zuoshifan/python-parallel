# array_io.py

"""
Demonstrates how to access arrays stored in file.

Run this with 6 processes like:
$ mpiexec -n 6 python array_io.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# create a 2 x 3 Cartesian process grid
cart_comm = comm.Create_cart([2, 3])
# get the row and column coordinate of each process in the process grid
ri, ci = cart_comm.Get_coords(rank)

# the global array
global_ary = np.arange(10*12, dtype='i').reshape(10, 12)
rs, re = 5*ri, 5*(ri+1) # start and end of row
cs, ce = 4*ci, 4*(ci+1) # start and end of column
# local array of each process
local_ary = np.ascontiguousarray(global_ary[rs:re, cs:ce])
print 'rank %d has local_ary with shape %s' % (rank, local_ary.shape)

filename = 'temp.txt'

# -------------------------------------------------------------------------------
# use darray type

# open the file for read and write, create it if it does not exist,
# and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

# the etype
etype = MPI.INT

# construct filetype
gsizes = [10, 12] # global shape of the array
distribs = [MPI.DISTRIBUTE_BLOCK, MPI.DISTRIBUTE_BLOCK] # block distribution in both dimensions
dargs = [MPI.DISTRIBUTE_DFLT_DARG, MPI.DISTRIBUTE_DFLT_DARG] # default distribution args
psizes = [2, 3] # process grid in C order
filetype = MPI.INT.Create_darray(6, rank, gsizes, distribs, dargs, psizes)
filetype.Commit()

# set the file view
fh.Set_view(0, etype, filetype)

# collectively write the data to file
fh.Write_all(local_ary)

# reset file view
fh.Set_view(0, etype, etype)

# check what's in the file
if rank == 0:
    buf = np.zeros(10 * 12, dtype='i').reshape(10, 12)
    fh.Read_at(0, buf)
    assert np.allclose(buf, global_ary)

# close the file
fh.Close()


# -------------------------------------------------------------------------------
# use subarray type

# open the file for read and write, create it if it does not exist,
# and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

# the etype
etype = MPI.INT

# construct filetype
gsizes = [10, 12] # global shape of the array
subsize = [5, 4] # shape of local subarray
starts = [rs, cs] # global indices of the first element of the local array
filetype = MPI.INT.Create_subarray(gsizes, subsize, starts)
filetype.Commit()

# set the file view
fh.Set_view(0, etype, filetype)

# collectively write the data to file
fh.Write_all(local_ary)

# reset file view
fh.Set_view(0, etype, etype)

# check what's in the file
if rank == 0:
    buf = np.zeros(10 * 12, dtype='i').reshape(10, 12)
    fh.Read_at(0, buf)
    assert np.allclose(buf, global_ary)

# close the file
fh.Close()


# -------------------------------------------------------------------------------
# use subarray type to access local array with ghost area

# create local array with one row and one column ghost area outside
local_ghost = np.zeros((7, 6), dtype='i')
local_ghost[1:6, 1:5] = local_ary # put local_ary in the center of local_ghost
# here you can fill in the ghost area, but data in ghost area will not be writen
# to file, so we omit it here...

# open the file for read and write, create it if it does not exist,
# and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

# the etype
etype = MPI.INT

# construct filetype
gsizes = [10, 12] # global shape of the array
subsize = [5, 4] # shape of local subarray
starts = [rs, cs] # global indices of the first element of the local array
filetype = MPI.INT.Create_subarray(gsizes, subsize, starts)
filetype.Commit()

# set the file view
fh.Set_view(0, etype, filetype)

# create a subarray type to describe the data located in local_phost without ghost area
memsize = local_ghost.shape
subsize = local_ary.shape
starts  = [1, 1]
memtype = MPI.INT.Create_subarray(memsize, subsize, starts)
memtype.Commit()

# collectively write the actual data inside local_ghost to file
fh.Write_all([local_ghost, 1, memtype])

# reset file view
fh.Set_view(0, etype, etype)

# check what's in the file
if rank == 0:
    buf = np.zeros(10 * 12, dtype='i').reshape(10, 12)
    fh.Read_at(0, buf)
    assert np.allclose(buf, global_ary)

# close the file
fh.Close()


# -------------------------------------------------------------------------------
# use map array to access irregularly distributed array

global_ary = np.arange(100, 124, dtype='i')
index_ary = np.arange(4*6, dtype='i')
# permutate the index array
if rank == 0:
    rand_index = np.random.permutation(index_ary)
else:
    rand_index = None
rand_index = comm.bcast(rand_index, root=0)
map_ary = np.sort(rand_index[4*rank:4*(rank+1)]) # map array should be nondecreasing
local_ary = global_ary[map_ary]
if rank == 0:
    print 'global_ary: %s' % global_ary
print 'rank %d has local_ary: %s, map_ary: %s' % (rank, local_ary, map_ary)

# open the file for read and write, create it if it does not exist,
# and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

# the etype
etype = MPI.INT

# construct filetype
filetype = MPI.INT.Create_indexed_block(1, displacements=map_ary)
filetype.Commit()

# set the file view
fh.Set_view(0, etype, filetype)

# collectively write the data to file
fh.Write_all(local_ary)

# reset file view
fh.Set_view(0, etype, etype)

# check what's in the file
if rank == 0:
    buf = np.zeros(24, dtype='i')
    fh.Read_at(0, buf)
    assert np.allclose(buf, global_ary)

# close the file
fh.Close()