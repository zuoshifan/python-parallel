# Sendrecv_replace.py

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

print 'process %d sends %s' % (rank, send_buf)
comm.Sendrecv_replace(send_buf, dest=right, sendtag=tag, source=left, recvtag=tag)
print 'process %d receives %s' % (rank, send_buf)
