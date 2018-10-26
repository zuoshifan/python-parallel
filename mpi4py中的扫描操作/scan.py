# scan.py

"""
Demonstrates the usage of scan, exscan, Scan, Exscan.

Run this with 4 processes like:
$ mpiexec -n 4 python scan.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# ------------------------------------------------------------------------------
# scan
send_obj = [2.5, 0.5, 3.5, 1.5][rank]
recv_obj = comm.scan(send_obj)
# scan by SUM:
# rank 0: 2.5
# rank 1: 2.5 + 0.5 = 3.0
# rank 2: 2.5 + 0.5 + 3.5 = 6.5
# rank 3: 2.5 + 0.5 + 3.5 + 1.5 = 8.0
print 'scan with SUM: rank %d has %s' % (rank, recv_obj)
recv_obj = comm.scan(send_obj, op=MPI.MAX)
# scan by MAX:
# rank 0: 2.5
# rank 1: max(2.5, 0.5) = 2.5
# rank 2: max(2.5, 0.5, 3.5) = 3.5
# rank 3: max(2.5, 0.5, 3.5, 1.5) = 3.5
print 'scan with MAX: rank %d has %s' % (rank, recv_obj)


# ------------------------------------------------------------------------------
# exscan
recv_obj = comm.exscan(send_obj)
# scan by SUM:
# rank 0: None
# rank 1: 2.5
# rank 2: 2.5 + 0.5 = 3.0
# rank 3: 2.5 + 0.5 + 3.5 = 6.5
print 'exscan with SUM: rank %d has %s' % (rank, recv_obj)
recv_obj = comm.exscan(send_obj, op=MPI.MAX)
# scan by MAX:
# rank 0: None
# rank 1: 2.5
# rank 2: max(2.5, 0.5) = 2.5
# rank 3: max(2.5, 0.5, 3.5) = 3.5
print 'exscan with MAX: rank %d has %s' % (rank, recv_obj)


# ------------------------------------------------------------------------------
# Scan
send_buf = np.array([0, 1], dtype='i') + 2 * rank
recv_buf = np.empty(2, dtype='i')

comm.Scan(send_buf, recv_buf, op=MPI.SUM)
# Scan by SUM:
# rank 0: [0, 1]
# rank 1: [0, 1] + [2, 3] = [2, 4]
# rank 2: [0, 1] + [2, 3] + [4, 5] = [6, 9]
# rank 3: [0, 1] + [2, 3] + [4, 5] + [6, 7] = [12, 16]
print 'Scan by SUM: rank %d has %s' % (rank, recv_buf)

# ------------------------------------------------------------------------------
# Exscan
send_buf = np.array([0, 1], dtype='i') + 2 * rank
# initialize recv_buf with [-1, -1]
recv_buf = np.zeros(2, dtype='i') - 1

comm.Exscan(send_buf, recv_buf, op=MPI.SUM)
# Exscan by SUM:
# rank 0: [-1, -1]
# rank 1: [0, 1]
# rank 2: [0, 1] + [2, 3] = [2, 4]
# rank 3: [0, 1] + [2, 3] + [4, 5] = [6, 9]
print 'Exscan by SUM: rank %d has %s' % (rank, recv_buf)


# ------------------------------------------------------------------------------
# Scan with MPI.IN_PLACE
recv_buf = np.array([0, 1], dtype='i') + 2 * rank

comm.Scan(MPI.IN_PLACE, recv_buf, op=MPI.SUM)
# recv_buf used as both send buffer and receive buffer
# result same as Scan
print 'Scan by SUM with MPI.IN_PLACE: rank %d has %s' % (rank, recv_buf)


# ------------------------------------------------------------------------------
# Exscan with MPI.IN_PLACE
recv_buf = np.array([0, 1], dtype='i') + 2 * rank

comm.Exscan(MPI.IN_PLACE, recv_buf, op=MPI.SUM)
# recv_buf used as both send buffer and receive buffer
# rank 0: [0, 1]
# rank 1: [0, 1]
# rank 2: [0, 1] + [2, 3] = [2, 4]
# rank 3: [0, 1] + [2, 3] + [4, 5] = [6, 9]
print 'Exscan by SUM with MPI.IN_PLACE: rank %d has %s' % (rank, recv_buf)
