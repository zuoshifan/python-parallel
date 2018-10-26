# scalapy_demo.py

"""
Demonstrate the use of scalapy.

Run this with 4 process like:
$ mpiexec -n 4 python scalapy_demo.py
"""

import os
import numpy as np
import scipy.linalg as la
from mpi4py import MPI
from scalapy import core
import scalapy.routines as rt


comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size

if size != 4:
    raise Exception("Must run with 4 processes")

# define a function to compare whether two arrays are equal
allclose = lambda a, b: np.allclose(a, b, rtol=1e-4, atol=1e-6)

# initialize a global ProcessContext object,
# which includes the initialization of a 2 x 2 process grid
core.initmpi([2, 2], block_shape=[16, 16])

N = 300
# create a N x N numpy array with random numbers
gA = np.random.standard_normal((N, N)).astype(np.float64)
gA = np.asfortranarray(gA)
# create a DistributedMatrix from gA
dA = core.DistributedMatrix.from_global_array(gA, rank=0)
print 'rank %d has global_shape of dA = %s' % (rank, dA.global_shape)
print 'rank %d has local_shape of dA = %s' % (rank, dA.local_shape)
print 'rank %d has block_shape of dA = %s' % (rank, dA.block_shape)

# compute the inverse of dA
invA, ipiv = rt.inv(dA)
# convert to a global numpy array hold by rank 0 only
ginvA = invA.to_global_array(rank=0)

if rank == 0:
    # compare the result with that of scipy.linalg.inv
    print 'result equals that of scipy: ', allclose(ginvA, la.inv(gA))

# write dA to file
file_name = 'dA.dat'
dA.to_file(file_name)
# now read it from file and check it equals the original DistributedMatrix
dA1 = core.DistributedMatrix.from_file(file_name, dA.global_shape, dA.dtype, dA.block_shape, dA.context)
print 'rank %d has dA.local_array == dA1.local_array: %s' % (rank, allclose(dA.local_array, dA1.local_array))

# remove the file
if rank == 0:
    os.remove(file_name)
