# large_count.py

"""
Demonstrates the large counts in MPI-3.

Run this with 2 processes like:
$ mpiexec -n 2 python large_count.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.rank

MAX_INT32 = np.iinfo(np.int32).max
print 'Max value of a 32 bits int: %d' % MAX_INT32

# create a derived datatype conposed of MAX_INT32 MPI.INT
LARGE_TYPE = MPI.INT.Create_contiguous(MAX_INT32)
print 'LARGE_TYPE:', LARGE_TYPE.lb, LARGE_TYPE.ub, LARGE_TYPE.size, LARGE_TYPE.extent
# create a derived datatype conposed of 2*MAX_INT32 MPI.INT
LARGE_TYPE2 = LARGE_TYPE.Create_contiguous(2)
print 'LARGE_TYPE2:', LARGE_TYPE2.lb, LARGE_TYPE2.ub, LARGE_TYPE2.size, LARGE_TYPE2.extent

# commit the derived datatypes
LARGE_TYPE.Commit()
LARGE_TYPE2.Commit()

if rank == 0:
    large_array = np.ones(2*MAX_INT32, dtype=np.int32)
    print 'rank 0 sends a large message of', 1.0 * large_array.nbytes / 2**32, 'GB'
    # comm.Send([large_array, 1, LARGE_TYPE2], dest=1, tag=11)
    # or
    comm.Send([large_array, 2, LARGE_TYPE], dest=1, tag=11)
else:
    recv_buf = np.empty(2*MAX_INT32, dtype=np.int32)
    comm.Recv([recv_buf, 1, LARGE_TYPE2], source=0, tag=11)
    # or
    # comm.Recv([recv_buf, 2, LARGE_TYPE], source=0, tag=11)
    print 'rank 1 successfully received the large message.'
