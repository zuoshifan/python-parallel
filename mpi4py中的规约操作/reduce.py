# reduce.py

"""
Demonstrates the usage of reduce, Reduce.

Run this with 4 processes like:
$ mpiexec -n 4 python reduce.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# ------------------------------------------------------------------------------
# reduce generic object from each process to root by using reduce
if rank == 0:
    send_obj = 0.5
elif rank == 1:
    send_obj = 2.5
elif rank == 2:
    send_obj = 3.5
else:
    send_obj = 1.5

# reduce by SUM: 0.5 + 2.5 + 3.5 + 1.5 = 8.0
recv_obj = comm.reduce(send_obj, op=MPI.SUM, root=1)
print 'reduce by SUM: rank %d has %s' % (rank, recv_obj)
# reduce by MAX: max(0.5, 2.5, 3.5, 1.5) = 3.5
recv_obj = comm.reduce(send_obj, op=MPI.MAX, root=2)
print 'reduce by MAX: rank %d has %s' % (rank, recv_obj)


# ------------------------------------------------------------------------------
# reduce numpy arrays from each process to root by using Reduce
send_buf = np.array([0, 1], dtype='i') + 2 * rank
if rank == 2:
    recv_buf = np.empty(2, dtype='i')
else:
    recv_buf = None

# Reduce by SUM: [0, 1] + [2, 3] + [4, 5] + [6, 7] = [12, 16]
comm.Reduce(send_buf, recv_buf, op=MPI.SUM, root=2)
print 'Reduce by SUM: rank %d has %s' % (rank, recv_buf)


# ------------------------------------------------------------------------------
# reduce numpy arrays from each process to root by using Reduce with MPI.IN_PLACE
send_buf = np.array([0, 1], dtype='i') + 2 * rank
if rank == 2:
    # initialize recv_buf with [-1, -1]
    recv_buf = np.zeros(2, dtype='i') - 1
else:
    recv_buf = None

# Reduce by SUM with MPI.IN_PLACE: [0, 1] + [2, 3] + [-1, -1] + [6, 7] = [7, 10]
if rank == 2:
    comm.Reduce(MPI.IN_PLACE, recv_buf, op=MPI.SUM, root=2)
else:
    comm.Reduce(send_buf, recv_buf, op=MPI.SUM, root=2)
print 'Reduce by SUM with MPI.IN_PLACE: rank %d has %s' % (rank, recv_buf)