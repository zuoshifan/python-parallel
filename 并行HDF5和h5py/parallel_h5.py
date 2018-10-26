# parallel_h5.py

"""
Demonstrates how to use parallel HDF5 with h5py.

Run this with 4 processes like:
$ mpiexec -n 4 python h5py_demo.py
"""

import os
import numpy as np
import h5py
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size

N = 10
# N = 2**29

file_name = 'test.hdf5'
# create a new HDF5 file collectively
f = h5py.File(file_name, driver='mpio', comm=comm)
# use atomic mode
f.atomic = True
# create a new group collectively
f.create_group('grp')
# create a empty dataset in group "/grp" collectively
f.create_dataset('grp/dset', shape=(size, N), dtype=np.int32)
# set an attribute of the dataset grp/dset collectively
f['grp/dset'].attrs['a'] = 1

data = np.arange(N, dtype=np.int32)
# write data to dataset grp/dset
f['grp/dset'][rank, :] = data
# rank 0 changes a slice of the dataset individually
if rank == 0:
    f['grp/dset'][1, :] += data
# synchronize here
comm.Barrier()
# rank 2 reads the changed slice
if rank == 2:
    print f['grp/dset'][1, :]
# read the attrs
if rank == 1:
    print f['grp/dset'].attrs['a']

# close file collectively
f.close()

# remove the created file
if rank == 0:
    os.remove(file_name)