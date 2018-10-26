# Send_Recv.py

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

count = 10
send_buf = np.arange(count, dtype='i')
recv_buf = np.empty(count, dtype='i')

if rank == 0:
    comm.Send([send_buf, count, MPI.INT], dest=1, tag=11)
    # comm.Send([send_buf, MPI.INT], dest=1, tag=11)
    # comm.Send(send_buf, dest=1, tag=11)

    comm.Recv([recv_buf, count, MPI.INT], source=1, tag=22)
    # comm.Recv([recv_buf, MPI.INT], source=1, tag=22)
    # comm.Recv(recv_buf, source=1, tag=22)
elif rank == 1:
    comm.Recv([recv_buf, count, MPI.INT], source=0, tag=11)
    # comm.Recv([recv_buf, MPI.INT], source=0, tag=11)
    # comm.Recv(recv_buf, source=0, tag=11)

    comm.Send([send_buf, count, MPI.INT], dest=0, tag=22)
    # comm.Send([send_buf, MPI.INT], dest=0, tag=22)
    # comm.Send(send_buf, dest=0, tag=22)

print 'process %d receives %s' % (rank, recv_buf)