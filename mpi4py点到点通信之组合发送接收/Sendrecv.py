# Sendrecv.py

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

tag = 123
left = rank - 1 if rank >=1 else size - 1
right = rank + 1 if rank < size - 1 else 0

count = 10
send_buf = np.arange(count, dtype='i') + 10 * rank
recv_buf = np.empty(count, dtype='i')

comm.Sendrecv(send_buf, dest=right, sendtag=tag, recvbuf=recv_buf, source=left, recvtag=tag)
print 'process %d sends %s' % (rank, send_buf)
print 'process %d receives %s' % (rank, recv_buf)
