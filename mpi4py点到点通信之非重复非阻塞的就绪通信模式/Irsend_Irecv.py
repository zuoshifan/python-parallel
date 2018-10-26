# Irsend_Irecv.py

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

count = 10
send_buf = np.arange(count, dtype='i')
recv_buf = np.empty(count, dtype='i')

if rank == 0:
    send_req = comm.Irsend(send_buf, dest=1, tag=11)
    send_req.Wait()
    print 'process %d sends %s' % (rank, send_buf)
elif rank == 1:
    recv_req = comm.Irecv(recv_buf, source=0, tag=11)
    recv_req.Wait()
    print 'process %d receives %s' % (rank, recv_buf)