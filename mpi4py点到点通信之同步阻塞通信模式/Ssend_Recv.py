# Ssend_Recv.py

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

count = 10
send_buf = np.arange(count, dtype='i')
recv_buf = np.empty(count, dtype='i')

if rank == 0:
    comm.Ssend(send_buf, dest=1, tag=11)
    print 'process %d sends %s' % (rank, send_buf)
elif rank == 1:
    comm.Recv(recv_buf, source=0, tag=11)
    print 'process %d receives %s' % (rank, recv_buf)