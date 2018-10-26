# mpiarray_demo.py

"""
Demonstrates the usage of MPIArray, from_numpy_array, to_numpy_array,
to_hdf5, enumerate, redistribute, reshape, transpose, wrap.

Run this with 4 processes like:
$ mpiexec -n 4 python mpiarray_demo.py
"""

import os
import numpy as np
from caput import mpiutil
from caput.mpiarray import MPIArray


rank = mpiutil.rank
size = mpiutil.size

# construct a MPIArray with global_shape (5, 4, 3) and distribute axis 0
shape = (5, 4, 3)
dist_axis = 0
darr = MPIArray(global_shape=shape, axis=dist_axis, dtype=np.float32)
print 'rank %d has global_shape = %s, local_shape = %s, local_offset = %s' % (rank, darr.global_shape, darr.local_shape, darr.local_offset)

# from_numpy_array
nparr = np.arange(6*5*4).reshape(6, 5, 4)
darr1 = MPIArray.from_numpy_array(nparr, axis=0, root=None)
# to_numpy_array
nparr1 = darr1.to_numpy_array(root=0)
if rank == 0:
    print 'rank 0: nparr1 == nparr: %s' % np.allclose(nparr, nparr1)
else:
    print 'rank %d: nparr1 = %s' % (rank, nparr1)
# to_hdf5
h5_file = 'test.hdf5'
darr1.to_hdf5(h5_file, 'test', create=True)
# remove the file
if rank == 0:
    os.remove(h5_file)

# enumerate
for (li, gi) in darr1.enumerate(axis=0):
    print 'rank %d has (local_index, global_index) = (%d, %d) for axis 0' % (rank, li, gi)
# redistribute to axis 1
darr2 = darr1.redistribute(axis=1)
print 'rank %d has global_shape = %s, local_shape = %s after redistribute to axis 1' % (rank, darr2.global_shape, darr2.local_shape)
# reshape darr1 to have global_shape = (6, 20)
darr3 = darr1.reshape(None, 20)
# transpose darr1 to have global_shape = (5, 6, 4)
darr4 = darr2.transpose((1, 0, 2))

# wrap
if rank == 0:
    a = np.zeros((2, 3))
elif rank == 1:
    a = np.zeros((2, 3))
elif rank == 2:
    a = np.zeros((2, 2))
elif rank == 3:
    a = np.zeros((2, 2))
da = MPIArray.wrap(a, axis=1)
print 'rank %d has global_shape of da = %s' % (rank, da.global_shape)