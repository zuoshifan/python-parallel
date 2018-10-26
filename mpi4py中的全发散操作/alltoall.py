# alltoall.py

"""
Demonstrates the usage of alltoall, Alltoall, Alltoallv, Alltoallw.

Run this with 4 processes like:
$ mpiexec -n 4 python alltoall.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# ------------------------------------------------------------------------------
# alltoall
send_obj = [1.2, 'xy', {'a': 1}, (2,)]
recv_obj = comm.alltoall(send_obj)
print 'alltoall: rank %d has %s' % (rank, recv_obj)


# ------------------------------------------------------------------------------
# Alltoall
send_buf = np.arange(4, dtype='i')
recv_buf = np.empty(4, dtype='i')
comm.Alltoall(send_buf, recv_buf)
print 'Alltoall: rank %d has %s' % (rank, recv_buf)


# ------------------------------------------------------------------------------
# Alltoall with MPI.IN_PLACE
recv_buf = np.arange(4, dtype='i')
comm.Alltoall(MPI.IN_PLACE, recv_buf)
print 'Alltoall with MPI.IN_PLACE: rank %d has %s' % (rank, recv_buf)


# ------------------------------------------------------------------------------
# Alltoallv
send_buf = np.arange(8, dtype='i')
recv_buf = np.empty(8, dtype='i')
if rank == 0:
    send_cnt = [2, 3, 1, 2]
    send_dpl = [0, 2, 5, 6]
    recv_cnt = [2, 3, 2, 1]
    recv_dpl = [0, 2, 5, 7]
elif rank == 1:
    send_cnt = [3, 2, 2, 1]
    send_dpl = [0, 3, 5, 7]
    recv_cnt = [3, 2, 1, 2]
    recv_dpl = [0, 3, 5, 6]
elif rank == 2:
    send_cnt = [2, 1, 3, 2]
    send_dpl = [0, 2, 3, 6]
    recv_cnt = [1, 2, 3, 2]
    recv_dpl = [0, 1, 3, 6]
else:
    send_cnt = [1, 2, 2, 3]
    send_dpl = [0, 1, 3, 5]
    recv_cnt = [2, 1, 2, 3]
    recv_dpl = [0, 2, 3, 5]
# the matrix of recv_cnt should be the transpose of the matrix of send_cnt
#     [[2, 3, 1, 2],                    [[2, 3, 2, 1],
# A =  [3, 2, 2, 1],          B = A.T =  [3, 2, 1, 2],
#      [2, 1, 3, 2],                     [1, 2, 3, 2],
#      [1, 2, 2, 3]]                     [2, 1, 2, 3]]
comm.Alltoallv([send_buf, send_cnt, send_dpl, MPI.INT], [recv_buf, recv_cnt, recv_dpl, MPI.INT])
print 'Alltoallv: rank %d has %s' % (rank, recv_buf)


# ------------------------------------------------------------------------------
# Alltoallv with MPI.IN_PLACE
recv_buf = np.arange(8, dtype='i')
if rank == 0:
    cnt = [2, 3, 1, 2]
    dpl = [0, 2, 5, 6]
elif rank == 1:
    cnt = [3, 1, 2, 2]
    dpl = [0, 3, 4, 6]
elif rank == 2:
    cnt = [1, 2, 2, 3]
    dpl = [0, 1, 3, 5]
else:
    cnt = [2, 2, 3, 1]
    dpl = [0, 2, 4, 6]
# with MPI.IN_PLACE, the maxtrix of cnt should be symmetric
#            [[2, 3, 1, 2],
# A = A.T =   [3, 1, 2, 2],
#             [1, 2, 2, 3],
#             [2, 2, 3, 1]]
comm.Alltoallv(MPI.IN_PLACE, [recv_buf, cnt, dpl, MPI.INT])
print 'Alltoallv with MPI.IN_PLACE: rank %d has %s' % (rank, recv_buf)


# ------------------------------------------------------------------------------
# Alltoallw example 1
send_buf = bytearray(b"abcd")
recv_buf = bytearray(4)
cnt = [1, 1, 1, 1]
dpl = [0, 1, 2, 3]
typ = [MPI.CHAR, MPI.CHAR, MPI.CHAR, MPI.CHAR]
comm.Alltoallw([send_buf, cnt, dpl, typ], [recv_buf, cnt, dpl, typ])
# or
# comm.Alltoallw([send_buf, (cnt, dpl), typ], [recv_buf, (cnt, dpl), typ])
print 'Alltoallw1: rank %d has %s' % (rank, recv_buf)

# Alltoallw example 2
# create a send buffer as a numpy structured array with elements with different types
send_buf = np.array([('a', 1, 1.5, 3.2)], dtype=[('a', 'c'), ('b', 'i4'), ('c', 'f4'), ('d', 'f8')])
send_cnt = [1, 1, 1, 1]
send_dpl = [0, 1, 5, 9]
send_typ = [MPI.CHAR, MPI.INT, MPI.FLOAT, MPI.DOUBLE]
if rank == 0:
    recv_buf = np.empty(4, dtype='c')
    recv_cnt = [1, 1, 1, 1]
    recv_dpl = [0, 1, 2, 3]
    recv_typ = [MPI.CHAR, MPI.CHAR, MPI.CHAR, MPI.CHAR]
elif rank == 1:
    recv_buf = np.empty(4, dtype='i4')
    recv_cnt = [1, 1, 1, 1]
    recv_dpl = [0, 4, 8, 12]
    recv_typ = [MPI.INT, MPI.INT, MPI.INT, MPI.INT]
if rank == 2:
    recv_buf = np.empty(4, dtype='f4')
    recv_cnt = [1, 1, 1, 1]
    recv_dpl = [0, 4, 8, 12]
    recv_typ = [MPI.FLOAT, MPI.FLOAT, MPI.FLOAT, MPI.FLOAT]
elif rank == 3:
    recv_buf = np.empty(4, dtype='f8')
    recv_cnt = [1, 1, 1, 1]
    recv_dpl = [0, 8, 16, 24]
    recv_typ = [MPI.DOUBLE, MPI.DOUBLE, MPI.DOUBLE, MPI.DOUBLE]

comm.Alltoallw([send_buf, send_cnt, send_dpl, send_typ], [recv_buf, recv_cnt, recv_dpl, recv_typ])
print 'Alltoallw2: rank %d has %s' % (rank, recv_buf)


# ------------------------------------------------------------------------------
# Alltoallw with MPI.IN_PLACE
if rank == 0:
    recv_buf = np.array([('a', 1, 1.5, 3.2)], dtype=[('a', 'c'), ('b', 'i4'), ('c', 'f4'), ('d', 'f8')])
    recv_cnt = [1, 1, 1, 1]
    recv_dpl = [0, 1, 5, 9]
    recv_typ = [MPI.CHAR, MPI.INT, MPI.FLOAT, MPI.DOUBLE]
if rank == 1:
    recv_buf = np.array([(2, 2.5, 4.2, 'b')], dtype=[('b', 'i4'), ('c', 'f4'), ('d', 'f8'), ('a', 'c')])
    recv_cnt = [1, 1, 1, 1]
    recv_dpl = [0, 4, 8, 16]
    recv_typ = [MPI.INT, MPI.FLOAT, MPI.DOUBLE, MPI.CHAR]
if rank == 2:
    recv_buf = np.array([(3.5, 5.2, 'c', 3)], dtype=[('c', 'f4'), ('d', 'f8'), ('a', 'c'), ('b', 'i4')])
    recv_cnt = [1, 1, 1, 1]
    recv_dpl = [0, 4, 12, 13]
    recv_typ = [MPI.FLOAT, MPI.DOUBLE, MPI.CHAR, MPI.INT]
if rank == 3:
    recv_buf = np.array([(6.2, 'd', 4, 4.5)], dtype=[('d', 'f8'), ('a', 'c'), ('b', 'i4'), ('c', 'f4')])
    recv_cnt = [1, 1, 1, 1]
    recv_dpl = [0, 8, 9, 13]
    recv_typ = [MPI.DOUBLE, MPI.CHAR, MPI.INT, MPI.FLOAT]

# with MPI.IN_PLACE, both the maxtrix of cnt and typ should be symmetric
#            [[1, 1, 1, 1],                [[c, i, f, d],
# A = A.T =   [1, 1, 1, 1],      B = B.T =  [i, f, d, c],
#             [1, 1, 1, 1],                 [f, d, c, i],
#             [1, 1, 1, 1]]                 [d, c, i, f]]
comm.Alltoallw(MPI.IN_PLACE, [recv_buf, recv_cnt, recv_dpl, recv_typ])
print 'Alltoallw with MPI.IN_PLACE: rank %d has %s' % (rank, recv_buf)