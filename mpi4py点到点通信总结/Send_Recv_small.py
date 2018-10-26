# Send_Recv_small.py

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

other = 1 if rank == 0 else 0

count = 10
# count = 1024 # will lead to dead lock
send_buf = np.arange(count, dtype='i')
recv_buf = np.empty(count, dtype='i')

print 'process %d trying sending...' % rank
comm.Send(send_buf, dest=other, tag=12)
print 'process %d trying receiving...' % rank
comm.Recv(recv_buf, source=other, tag=12)
print 'process %d done.' % rank
