# nbc.py

"""
Demonstrates nonblocking collective communication.

Run this with 4 processes like:
$ mpiexec -n 4 python nbc.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# ------------------------------------------------------------------------
# broadcast a numpy array by using Ibcast
if rank == 0:
    ary = np.arange(10, dtype='i')
else:
    ary = np.empty(10, dtype='i')

req = comm.Ibcast(ary, root=0)
req.Wait()
print 'Ibcast: rank %d has %s' % (rank, ary)


# ------------------------------------------------------------------------
# scatter a numpy array by using Iscatterv
if rank == 0:
    send_buf = np.arange(10, dtype='i')
    recv_buf = np.empty(4, dtype='i')
elif rank == 1:
    send_buf = None
    recv_buf = np.empty(3, dtype='i')
elif rank == 2:
    send_buf = None
    recv_buf = np.empty(2, dtype='i')
else:
    send_buf = None
    recv_buf = np.empty(1, dtype='i')
count = [4, 3, 2, 1]
displ = [0, 4, 7, 9]

req = comm.Iscatterv([send_buf, count, MPI.INT], recv_buf, root=0)
req.Wait()
print 'Iscatterv: rank %d has %s' % (rank, recv_buf)


# ------------------------------------------------------------------------
# Ialltoall
send_buf = np.arange(8, dtype='i')
recv_buf = np.empty(8, dtype='i')
req = comm.Ialltoall(send_buf, recv_buf)
req.Wait()
print 'Ialltoall: rank %d has %s' % (rank, recv_buf)