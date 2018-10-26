# send_recv_buf.py

import pickle
import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

send_obj = np.arange(10, dtype='i')
recv_buf = bytearray(2000) # pre-allocate a buffer for message receiving

if rank == 0:
    comm.send(send_obj, dest=1, tag=11)
elif rank == 1:
    recv_obj = comm.recv(recv_buf, source=0, tag=11)
    # print recv_buf
    print pickle.loads(recv_buf)

    print 'process %d receives %s' % (rank, recv_obj)
