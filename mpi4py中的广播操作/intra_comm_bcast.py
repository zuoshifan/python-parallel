# intra_comm_bcast.py

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# broadcast a generic object by using bcast
if rank == 1:
    obj = {'a': 1}
else:
    obj = None

obj = comm.bcast(obj, root=1)
print 'rank %d has %s' % (rank, obj)

# broadcast a numpy array by using Bcast
if rank == 2:
    ary = np.arange(10, dtype='i')
else:
    ary = np.empty(10, dtype='i')

comm.Bcast(ary, root=2)
print 'rank %d has %s' % (rank, ary)
