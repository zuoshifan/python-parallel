# Bsend_recv.py

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# MPI.BSEND_OVERHEAD gives the extra overhead in buffered mode
BUFSISE = 2000 + MPI.BSEND_OVERHEAD
buf = bytearray(BUFSISE)

# Attach a user-provided buffer for sending in buffered mode
MPI.Attach_buffer(buf)

count = 10
send_buf = np.arange(count, dtype='i')
recv_buf = np.empty(count, dtype='i')

if rank == 0:
    comm.Bsend(send_buf, dest=1, tag=11)
    comm.Recv(recv_buf, source=1, tag=22)
elif rank == 1:
    comm.Recv(recv_buf, source=0, tag=11)
    comm.Bsend(send_buf, dest=0, tag=22)

print 'process %d receives %s' % (rank, recv_buf)

# Remove an existing attached buffer
MPI.Detach_buffer()