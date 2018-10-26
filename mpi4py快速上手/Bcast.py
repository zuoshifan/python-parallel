# Bcast.py

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    data = np.arange(10, dtype='i')
    print 'before broadcasting: process %d has %s' % (rank, data)
else:
    data = np.zeros(10, dtype='i')
    print 'before broadcasting: process %d has %s' % (rank, data)

comm.Bcast(data, root=0)

print 'after broadcasting: process %d has %s' % (rank, data)