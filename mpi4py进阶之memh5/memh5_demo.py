# memh5_demo.py

"""
Demonstrates how to use memh5.

Run this with 4 processes like:
$ mpiexec -n 4 python memh5_demo.py
"""

import os
import numpy as np
import h5py
from mpi4py import MPI
from caput import memh5


comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size

N = 10
data = np.arange(N, dtype=np.int32)

file_name = 'test.hdf5'
# create a new HDF5 file collectively
f = h5py.File(file_name, driver='mpio', comm=comm)
# use atomic mode
f.atomic = True
# create a new group collectively
f.create_group('grp')
# create a dataset in group "/grp" collectively
f.create_dataset('grp/dset', data=data)
# set an attribute of the dataset grp/dset collectively
f['grp/dset'].attrs['a'] = 1
# close file collectively
f.close()

# create MemGroup from the HDF5 file
mgrp = memh5.MemGroup.from_hdf5(file_name, distributed=True, comm=comm)
# create a new MemDatasetCommon
dset1 = mgrp.create_dataset('dset1', shape=(3, 4), dtype=np.float32)
print 'dset1.common = %s, dset1.distributed = %s' % (dset1.common, dset1.distributed)
# create a new MemDatasetDistributed
dset2 = mgrp.create_dataset('dset2', shape=(3, 4), dtype=np.float32, distributed=True, distributed_axis=1)
print 'dset2.common = %s, dset2.distributed = %s, dset2.distributed_axis = %d' % (dset2.common, dset2.distributed, dset2.distributed_axis)
# redistribute dset2 to axis 0
dset2.redistribute(axis=0)
print 'after redistribute, dset2.distributed_axis = %d' %  dset2.distributed_axis
# change dset2 to be MemDatasetCommon
mgrp.dataset_distributed_to_common('dset2')
# create and set an attribute of dset2
dset2.attrs['status'] = 'new crated'
# write mgrp to a HDF5 file
mgrp.to_hdf5('new.hdf5')

# remove the created files
if rank == 0:
    os.remove(file_name)
    os.remove('new.hdf5')