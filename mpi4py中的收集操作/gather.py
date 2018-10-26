# gather.py

"""
Demonstrates the usage of gather, Gather, Gatherv.

Run this with 4 processes like:
$ mpiexec -n 4 python gather.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# ------------------------------------------------------------------------------
# gather generic object from each process to root by using gather
if rank == 0:
    send_obj = 1.2
elif rank == 1:
    send_obj = 'xxx'
elif rank == 2:
    send_obj = {'a': 1}
else:
    send_obj = (2,)

recv_obj = comm.gather(send_obj, root=1)
print 'gather: rank %d has %s' % (rank, recv_obj)


# ------------------------------------------------------------------------------
# gather same length numpy arrays from each process to root by using Gather
send_buf = np.array([0, 1], dtype='i') + 2 * rank
if rank == 2:
    recv_buf = np.empty(8, dtype='i')
else:
    recv_buf = None

comm.Gather(send_buf, recv_buf, root=2)
print 'Gather: rank %d has %s' % (rank, recv_buf)


# ------------------------------------------------------------------------------
# gather same length numpy arrays from each process to root by using Gather with MPI.IN_PLACE
send_buf = np.array([0, 1], dtype='i') + 2 * rank
if rank == 2:
    # initialize a receive buffer with all -1
    recv_buf = np.zeros(8, dtype='i') - 1
else:
    recv_buf = None

# each process other than the root sends two numbers of send_buf to root
# but the root does not sends message to itself with MPI.IN_PLACE
#     rank 0   |   rank 1   |   rank 2   |   rank 3
#  ------------+------------+------------+------------
#     [0, 1]   |   [2, 3]   |  [-1, -1]  |   [6. 7]
if rank == 2:
    comm.Gather(MPI.IN_PLACE, recv_buf, root=2)
else:
    comm.Gather(send_buf, recv_buf, root=2)
print 'Gather: rank %d has %s with MPI.IN_PLACE' % (rank, recv_buf)


# ------------------------------------------------------------------------------
# gather a numpy array from each process to the root by using Gatherv
if rank == 0:
    send_buf = np.array([10, 11, 12], dtype='i')
elif rank == 1:
    send_buf = np.array([13], dtype='i')
elif rank == 2:
    send_buf = np.array([14, 15, 16, 17], dtype='i')
else:
    send_buf = np.array([18, 19], dtype='i')
if rank == 2:
    recv_buf = np.empty(10, dtype='i')
else:
    recv_buf = None
count = [3, 1, 4, 2]
displ = [0, 3, 4, 8]
# gather numpy arrays with different length to the root from each process with allocation:
#          rank 0   |   rank 1   |   rank 2    |   rank 3
#        -----------+------------+-------------+-------------
#         10 11 12  |     13     | 14 15 16 17 |   18 19
# displ:  0               3        4               8

comm.Gatherv(send_buf, [recv_buf, count, displ, MPI.INT], root=2)
print 'Gatherv: rank %d has %s' % (rank, recv_buf)
