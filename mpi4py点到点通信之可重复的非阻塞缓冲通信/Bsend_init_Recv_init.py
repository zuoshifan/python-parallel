# Bsend_init_Recv_init.py

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
    send_req = comm.Bsend_init(send_buf, dest=1, tag=11)
    send_req.Start()
    send_req.Wait()
    print 'process %d sends %s' % (rank, send_buf)
elif rank == 1:
    recv_req = comm.Recv_init(recv_buf, source=0, tag=11)
    recv_req.Start()
    recv_req.Wait()
    print 'process %d receives %s' % (rank, recv_buf)

# Remove an existing attached buffer
MPI.Detach_buffer()