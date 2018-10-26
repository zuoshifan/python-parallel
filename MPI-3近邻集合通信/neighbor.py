# neighbor.py

"""
Demonstrates the usage of neighborhood collective communication.

Run this with 9 processes like:
$ mpiexec -n 9 python neighbor.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

dims = [3, 3]

# -----------------------------------------------------------------
# neighbor_allgather with periodic boundary
periods = [True, True]
cart_comm = comm.Create_cart(dims, periods)
recv_obj = cart_comm.neighbor_allgather(rank)
print 'neighbor_allgather (periodic): rank %d has %s' % (rank, recv_obj)


# -----------------------------------------------------------------
# neighbor_allgather with non-periodic boundary
periods = [False, False]
cart_comm = comm.Create_cart(dims, periods)
recv_obj = cart_comm.neighbor_allgather(rank)
print 'neighbor_allgather (non-periodic): rank %d has %s' % (rank, recv_obj)


# -----------------------------------------------------------------
# neighbor_alltoall with periodic boundary
periods = [True, True]
cart_comm = comm.Create_cart(dims, periods)
recv_obj = cart_comm.neighbor_alltoall(['a', 'b', 'c', 'd'])
print 'neighbor_alltoall (periodic): rank %d has %s' % (rank, recv_obj)


# -----------------------------------------------------------------
# Neighbor_allgather with periodic boundary
periods = [True, True]
cart_comm = comm.Create_cart(dims, periods)
send_buf = np.array([rank], dtype='i')
recv_buf = np.full((4,), -1, dtype='i') # initialize with all -1
cart_comm.Neighbor_allgather(send_buf, recv_buf)
print 'Neighbor_allgather (periodic): rank %d has %s' % (rank, recv_buf)


# -----------------------------------------------------------------
# Ineighbor_allgather with non-periodic boundary
periods = [False, False]
cart_comm = comm.Create_cart(dims, periods)
send_buf = np.array([rank], dtype='i')
recv_buf = np.full((4,), -1, dtype='i')
req = cart_comm.Ineighbor_allgather(send_buf, recv_buf)
req.Wait()
print 'Ineighbor_allgather (non-periodic): rank %d has %s' % (rank, recv_buf)