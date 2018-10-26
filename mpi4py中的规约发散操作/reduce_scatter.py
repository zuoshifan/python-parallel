# reduce_scatter.py

"""
Demonstrates the usage of Reduce_scatter_block, Reduce_scatter.

Run this with 4 processes like:
$ mpiexec -n 4 python reduce_scatter.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()


# ------------------------------------------------------------------------------
# reduce scatter a numpy array by using Reduce_scatter_block
send_buf = np.arange(8, dtype='i')
recv_buf = np.empty(2, dtype='i')

# first step: reduce
# rank 0  |  0  1  2  3  4  5  6  7
# rank 1  |  0  1  2  3  4  5  6  7
# rank 2  |  0  1  2  3  4  5  6  7
# rank 3  |  0  1  2  3  4  5  6  7
# --------+-------------------------
# SUM     |  0  4  8  12 16 20 24 28
# second step: scatter
#  rank 0  |  rank 1  | rank 2  |  rank 3
# ---------+----------+---------+---------
#   0 4    |   8 12   |  16 20  |  24 28
comm.Reduce_scatter_block(send_buf, recv_buf, op=MPI.SUM)
print 'Reduce_scatter_block by SUM: rank %d has %s' % (rank, recv_buf)

# ------------------------------------------------------------------------------
# reduce scatter a numpy array by using Reduce_scatter_block with MPI.IN_PLACE
recv_buf = np.arange(8, dtype='i')

# with MPI.IN_PLACE, recv_buf is used as both send buffer and receive buffer
# the first two elements of recv_buf will be filled with the scattered results
comm.Reduce_scatter_block(MPI.IN_PLACE, recv_buf, op=MPI.SUM)
print 'Reduce_scatter_block by SUM with MPI.IN_PLACE: rank %d has %s' % (rank, recv_buf)

# ------------------------------------------------------------------------------
# reduce scatter a numpy array by using Reduce_scatter
send_buf = np.arange(8, dtype='i')
recvcounts = [2, 3, 1, 2]
recv_buf = np.empty(recvcounts[rank], dtype='i')

# first step: reduce
# rank 0  |  0  1  2  3  4  5  6  7
# rank 1  |  0  1  2  3  4  5  6  7
# rank 2  |  0  1  2  3  4  5  6  7
# rank 3  |  0  1  2  3  4  5  6  7
# --------+-------------------------
# SUM     |  0  4  8  12 16 20 24 28
# second step: scatterv with [2, 3, 1, 2]
#  rank 0  |  rank 1  | rank 2  |  rank 3
# ---------+----------+---------+---------
#   0 4    |  8 12 16 |   20    |  24 28
comm.Reduce_scatter(send_buf, recv_buf, recvcounts=[2, 3, 1, 2], op=MPI.SUM)
print 'Reduce_scatter by SUM: rank %d has %s' % (rank, recv_buf)
