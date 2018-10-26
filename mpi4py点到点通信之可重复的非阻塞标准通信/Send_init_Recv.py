# Send_init_Recv.py

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

count = 10
send_buf = np.arange(count, dtype='i') + 10 * rank
recv_buf = np.empty((size - 1, count), dtype='i')

if rank != 0:
    send_req = comm.Send_init(send_buf, dest=0, tag=rank)
    send_req.Start()
    send_req.Wait()
    print 'process %d sends %s' % (rank, send_buf)
else:
    for i in range(size - 1):
        comm.Recv(recv_buf[i], source=i+1, tag=i+1)
        print 'process %d receives %s' % (rank, recv_buf[i])