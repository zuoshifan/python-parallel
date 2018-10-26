# allreduce.py

"""
Demonstrates the usage of allreduce, Allreduce.

Run this with 4 processes like:
$ mpiexec -n 4 python allreduce.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# ------------------------------------------------------------------------------
# reduce generic object from each process by using allreduce
if rank == 0:
    send_obj = 0.5
elif rank == 1:
    send_obj = 2.5
elif rank == 2:
    send_obj = 3.5
else:
    send_obj = 1.5

# reduce by SUM: 0.5 + 2.5 + 3.5 + 1.5 = 8.0
recv_obj = comm.allreduce(send_obj, op=MPI.SUM)
print 'allreduce by SUM: rank %d has %s' % (rank, recv_obj)
# reduce by MAX: max(0.5, 2.5, 3.5, 1.5) = 3.5
recv_obj = comm.allreduce(send_obj, op=MPI.MAX)
print 'allreduce by MAX: rank %d has %s' % (rank, recv_obj)


# ------------------------------------------------------------------------------
# reduce numpy arrays from each process by using Allreduce
send_buf = np.array([0, 1], dtype='i') + 2 * rank
recv_buf = np.empty(2, dtype='i')

# Reduce by SUM: [0, 1] + [2, 3] + [4, 5] + [6, 7] = [12, 16]
comm.Allreduce(send_buf, recv_buf, op=MPI.SUM)
print 'Allreduce by SUM: rank %d has %s' % (rank, recv_buf)


# ------------------------------------------------------------------------------
# reduce numpy arrays from each process by using Allreduce with MPI.IN_PLACE
recv_buf = np.array([0, 1], dtype='i') + 2 * rank

# Reduce by SUM with MPI.IN_PLACE: [0, 1] + [2, 3] + [5, 6] + [6, 7] = [12, 16]
# recv_buf used as both send buffer and receive buffer
comm.Allreduce(MPI.IN_PLACE, recv_buf, op=MPI.SUM)
print 'Allreduce by SUM with MPI.IN_PLACE: rank %d has %s' % (rank, recv_buf)
