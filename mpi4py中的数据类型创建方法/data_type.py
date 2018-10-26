# data_type.py

"""
Demonstrates the usage of Create_contiguous, Create_vector, Create_hvector,
Create_indexed, Create_hindexed, Create_struct, Create_subarray, Commit, Free.

Run this with 4 processes like:
$ mpiexec -n 4 python data_type.py
"""

import os
import shutil
import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# ------------------------------------------------------------------------------
# Create_contiguous
# create a contiguous data type by copying MPI.INT 4 times
INT4 = MPI.INT.Create_contiguous(4)
print 'INT4:', INT4.lb, INT4.ub, INT4.size, INT4.extent

# in the following, B: one byte empty space

# ------------------------------------------------------------------------------
# Create_vector, Create_hvector
# create a vector data type from MPI.FLOAT with count = 2, blocklength = 3, stride = 4
# FLOAT_vector: [FLOAT FLOAT FLOAT] B B B B [FLOAT FLOAT FLOAT]
# blocklength:           3                           3
# stride:        0                           4
FLOAT_vector = MPI.FLOAT.Create_vector(2, 3, 4)
print 'FLOAT_vector:', FLOAT_vector.lb, FLOAT_vector.ub, FLOAT_vector.size, FLOAT_vector.extent
# FLOAT_hvector = MPI.FLOAT.Create_hvector(2, 3, 4*4)
# print 'FLOAT_hvector:', FLOAT_hvector.lb, FLOAT_hvector.ub, FLOAT_hvector.size, FLOAT_hvector.extent

# ------------------------------------------------------------------------------
# Create_indexed, Create_hindexed
# create a indexed data type from MPI.INT with blocklengths = [2, 3], displacements = [0, 4]
# INT_indexed:   [INT INT] B B B B B B B B [INT INT INT]
# blocklengths:      2                           3
# displacements:  0                         4
INT_indexed = MPI.INT.Create_indexed([2, 3], [0, 4])
print 'INT_indexed:', INT_indexed.lb, INT_indexed.ub, INT_indexed.size, INT_indexed.extent
# INT_hindexed = MPI.INT.Create_hindexed([2, 3], [0, 4*4])
# print 'INT_hindexed:', INT_hindexed.lb, INT_hindexed.ub, INT_hindexed.size, INT_hindexed.extent

# ------------------------------------------------------------------------------
# Create_struct
# create a struct data type with blocklengths = [2, 3], displacements = [0, 6], datatypes = [MPI.CHAR, MPI.INT]
# TYPE_struct:   [CHAR CHAR] B B B B [INT INT INT]
# blocklengths:       2                    3
# displacements:  0                   6
# datatypes:        CHAR                  INT
TYPE_struct = MPI.Datatype.Create_struct([2, 3], [0, 6], [MPI.CHAR, MPI.INT])
print 'TYPE_struct:', TYPE_struct.lb, TYPE_struct.ub, TYPE_struct.size, TYPE_struct.extent, TYPE_struct.true_lb, TYPE_struct.true_ub, TYPE_struct.true_extent

# ------------------------------------------------------------------------------
# Create_subarray
sizes = (2, 8) # a 2-dimensional array with 2 rows and 8 columns
if rank == 0:
    # the first 3 columns
    subsizes = (2, 3)
    starts = (0, 0)
elif rank == 1:
    # the nest 2 columns
    subsizes = (2, 2)
    starts = (0, 3)
elif rank == 2:
    # the nest 1 column
    subsizes = (2, 1)
    starts = (0, 5)
elif rank == 3:
    # the last 2 columns
    subsizes = (2, 2)
    starts = (0, 6)
INT_subarray = MPI.INT.Create_subarray(sizes, subsizes, starts)
print 'INT_subarray:', INT_subarray.lb, INT_subarray.ub, INT_subarray.size, INT_subarray.extent

# ------------------------------------------------------------------------------
# gather subarrays from all processes by using the defined INT_subarray
if rank == 0:
    full_array = np.empty((2, 8), dtype='i')
    subarray = np.array([[0, 1, 2], [8, 9, 10]], dtype='i')
elif rank == 1:
    full_array = None
    subarray = np.array([[3, 4], [11, 12]], dtype='i')
elif rank == 2:
    full_array = None
    subarray = np.array([[5], [13]], dtype='i')
elif rank == 3:
    full_array = None
    subarray = np.array([[6, 7], [14, 15]], dtype='i')

subsizes = comm.gather(subsizes, root=0)
starts = comm.gather(starts, root=0)
# each process sends subarray to rank 0
print 'rank %d sends:' % rank, subarray
sreq = comm.Isend(subarray, dest=0, tag=0)
# rank 0 receives subarray from each process and put them into full_array
if rank == 0:
    # create new data type INT_subarray and commit them
    subtypes = [ MPI.INT.Create_subarray(sizes, subsize, start).Commit() for (subsize, start) in zip(subsizes, starts) ]
    for i in range(size):
        comm.Recv([full_array, subtypes[i]], source=i, tag=0)
    # free the new data type INT_subarray
    [ subtype.Free() for subtype in subtypes ]

# wait for complete
sreq.Wait()
if rank == 0:
    print 'rank 0 receives:', full_array
