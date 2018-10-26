# Scatter.py

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

sendbuf = None
if rank == 0:
    sendbuf = np.empty([size, 10], dtype='i')
    sendbuf.T[:, :] = range(size)
print 'before scattering: process %d has %s' % (rank, sendbuf)

recvbuf = np.empty(10, dtype='i')
comm.Scatter(sendbuf, recvbuf, root=0)
print 'after scattering: process %d has %s' % (rank, recvbuf)