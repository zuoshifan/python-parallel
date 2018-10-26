# Gather.py

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

sendbuf = np.zeros(10, dtype='i') + rank
print 'before gathering: process %d has %s' % (rank, sendbuf)

recvbuf = None
if rank == 0:
    recvbuf = np.empty([size, 10], dtype='i')

comm.Gather(sendbuf, recvbuf, root=0)
print 'after gathering: process %d has %s' % (rank, recvbuf)