# Calls to attach and detach buffers

# from mpi4py import MPI
# try:
#     from numpy import empty
# except ImportError:
#     from array import array
#     def empty(size, dtype):
#         return array(dtype, [0]*size)


# BUFSISE = 10000 + MPI.BSEND_OVERHEAD

# buff = empty(BUFSISE, dtype='b')

# MPI.Attach_buffer(buff)

# buff2 = MPI.Detach_buffer()
# print len(buff2)

# MPI.Attach_buffer(buff2)
# print len(buff2)

# MPI.Detach_buffer()


# assert len(buff2) == BUFSISE


# ---------------------------------------------------------------


# from mpi4py import MPI


# BUFSISE = 10000 + MPI.BSEND_OVERHEAD

# buff = bytearray(BUFSISE)
# MPI.Attach_buffer(buff)
# MPI.Detach_buffer()



# ---------------------------------------------------------------


"""
Simple exchange of messages between two processes, using
buffered mode.

This should not deadlock.

HOWEVER, we can flood it if not checking somehow for message
delivery!

Run this with only two processes.

"""
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nproc = comm.Get_size()

if nproc != 2 and rank == 0:
    print('\n+\n+++ This program must be run with two processes only,'
          'not {}\n+\n'.format(nproc))
    comm.Abort(1)

K=1024
M=K*K
MAXMSGSIZE = 32*M

# We need at least two big messages, for safety!
MPIBUFF = np.empty((2*MAXMSGSIZE+K,), np.float64)
MPI.Attach_buffer(MPIBUFF)

bigBuff = np.empty((MAXMSGSIZE,), np.float64)

# Both processes do the same.
# This possibly just works up to a certain size
msgSize = 1
tag = 0
while msgSize <= MAXMSGSIZE:
    msg = np.random.random((msgSize,))
    sbuff = (msg, msgSize, MPI.DOUBLE_PRECISION)
    if rank == 0: print('\n** Trying with size: ', msgSize)
    comm.Bsend(msg, (rank+1)%2, tag)
    comm.Recv(bigBuff, (rank+1)%2, tag)

    if rank == 0:
        print('** Completed with size: ', msgSize)
    msgSize *= 2
    tag += 1 # This is unecessary, of course.

# THIS IS NOT NORMALLY NECESSARY!
MPI.Detach_buffer()