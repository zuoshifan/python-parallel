# attach_detach_buf.py

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

max_msg_size = 2**10
BUFSISE = 32 * max_msg_size
mpi_buf = bytearray(BUFSISE)

# Attach a big user-provided buffer for sending in buffered mode
MPI.Attach_buffer(mpi_buf)

recv_buf = np.empty((max_msg_size,), np.float64)

if rank == 0:
    print '-' * 80
    print 'With an attached big buffer:'
    print

msg_size = 1
tag = 0
while msg_size <= max_msg_size:
    msg = np.random.random((msg_size,))
    if rank == 0:
        print 'Trying with size: ', msg_size

    comm.Bsend(msg, (rank+1)%2, tag)
    comm.Recv(recv_buf, (rank+1)%2, tag)

    if rank == 0:
        print 'Completed with size: ', msg_size

    msg_size *= 2
    tag += 1

# Remove an existing attached buffer
MPI.Detach_buffer()

if rank == 0:
    print
    print '-' * 80
    print 'Without an attached big buffer:'
    print

msg_size = 1
tag = 0
while msg_size <= max_msg_size:
    msg = np.random.random((msg_size,))
    if rank == 0:
        print 'Trying with size: ', msg_size

    comm.Bsend(msg, (rank+1)%2, tag)
    comm.Recv(recv_buf, (rank+1)%2, tag)

    if rank == 0:
        print 'Completed with size: ', msg_size

    msg_size *= 2
    tag += 1
