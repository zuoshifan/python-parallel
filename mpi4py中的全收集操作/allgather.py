# allgather.py

"""
Demonstrates the usage of allgather, Allgather, Allgatherv.

Run this with 4 processes like:
$ mpiexec -n 4 python allgather.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# ------------------------------------------------------------------------------
# gather generic object from each process by using allgather
if rank == 0:
    send_obj = 1.2
elif rank == 1:
    send_obj = 'xxx'
elif rank == 2:
    send_obj = {'a': 1}
else:
    send_obj = (2,)

recv_obj = comm.allgather(send_obj)
print 'allgather: rank %d has %s' % (rank, recv_obj)


# ------------------------------------------------------------------------------
# gather same length numpy arrays from each process by using Allgather
send_buf = np.array([0, 1], dtype='i') + 2 * rank
recv_buf = np.empty(8, dtype='i')

comm.Allgather(send_buf, recv_buf)
print 'Allgather: rank %d has %s' % (rank, recv_buf)


# ------------------------------------------------------------------------------
# gather same length numpy arrays from each process by using Allgather with MPI.IN_PLACE
# initialize a receive buffer for each process
recv_buf = np.zeros(8, dtype='i') - 1
if rank == 0:
    recv_buf[:2] = np.array([0, 1]) # [0, 1, -1, -1, -1, -1, -1, -1]
elif rank == 1:
    recv_buf[2:4] = np.array([2, 3]) # [-1, -1, 2, 3, -1, -1, -1, -1]
elif rank == 2:
    recv_buf[4:6] = np.array([4, 5]) # [-1, -1, -1, -1, 4, 5, -1, -1]
elif rank == 3:
    recv_buf[6:] = np.array([6, 7]) # [ -1, -1, -1, -1, -1, -1, 6, 7]

# with MPI.IN_PLACE, recv_buf is used as both a send and a receive buffer
comm.Allgather(MPI.IN_PLACE, recv_buf)
print 'Allgather: rank %d has %s with MPI.IN_PLACE' % (rank, recv_buf)


# ------------------------------------------------------------------------------
# gather numpy array with different length from each process by using Gatherv
if rank == 0:
    send_buf = np.array([10, 11, 12], dtype='i')
elif rank == 1:
    send_buf = np.array([13], dtype='i')
elif rank == 2:
    send_buf = np.array([14, 15, 16, 17], dtype='i')
else:
    send_buf = np.array([18, 19], dtype='i')
recv_buf = np.empty(10, dtype='i')
count = [3, 1, 4, 2]
displ = [0, 3, 4, 8]
# gather numpy arrays with different length to the root from each process with allocation:
#          rank 0   |   rank 1   |   rank 2    |   rank 3
#        -----------+------------+-------------+-------------
#         10 11 12  |     13     | 14 15 16 17 |   18 19
# displ:  0               3        4               8

comm.Allgatherv(send_buf, [recv_buf, count, displ, MPI.INT])
print 'Allgatherv: rank %d has %s' % (rank, recv_buf)
