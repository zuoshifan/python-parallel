# status.py

"""
Demonstrates the usage of MPI.Status.

Run this with 2 processes like:
$ mpiexec -n 2 python status.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.rank

status = MPI.Status()
print 'status.source == MPI.ANY_SOURCE:', status.source == MPI.ANY_SOURCE
print 'status.tag == MPI.ANY_TAG:', status.tag == MPI.ANY_TAG
print 'status.error == MPI.SUCCESS:', status.error == MPI.SUCCESS
print 'MPI.UNDEFINED = %d' % MPI.UNDEFINED

comm.Barrier()

if rank == 0:
    send_buf = np.arange(10, dtype='i')
    # send 10 MPI.INTs, 40 MPI.BYTEs
    comm.Send(send_buf, dest=1, tag=0)

    # create a datatype and send it (multiple of sizeof(int))
    send_type = MPI.Datatype.Create_struct([1, 16], [0, 4], [MPI.INT, MPI.CHAR])
    send_type.Commit()
    # send 1 MPI.INT, 16 MPI.CHARs (= 4 MPI.INTs), 1 + 16 basic elements
    comm.Send([send_buf, 1, send_type], dest=1, tag=1)
    send_type.Free()

    # create a datatype and send it (not a multiple of sizeof(int))
    send_type = MPI.Datatype.Create_struct([1, 17], [0, 4], [MPI.INT, MPI.CHAR])
    send_type.Commit()
    # send 1 MPI.INT, 17 MPI.CHARs (not a multiple of MPI.INT), 1 + 17 basic elements
    comm.Send([send_buf, 1, send_type], dest=1, tag=2)
    send_type.Free()
elif rank == 1:
    recv_buf = np.full(10, -1, dtype='i')
    # receive 10 ints
    status = MPI.Status()
    comm.Recv(recv_buf, source=0, tag=0, status=status)
    print
    print 'Get count with MPI.INT:', status.Get_count(MPI.INT)
    print 'Get elements with MPI.INT:', status.Get_elements(MPI.INT)
    print 'Get count with MPI.BYTE:', status.Get_count(MPI.BYTE)
    print 'Get elements with MPI.BYTE:', status.Get_elements(MPI.BYTE)
    print

    # create a datatype and receive it
    recv_type = MPI.Datatype.Create_struct([1, 36], [0, 4], [MPI.INT, MPI.CHAR])
    recv_type.Commit()
    status = MPI.Status()
    comm.Recv([recv_buf, 1, recv_type], source=0, tag=1, status=status)
    print 'Get count with MPI.INT:', status.Get_count(MPI.INT)
    print 'Get elements with MPI.INT:', status.Get_elements(MPI.INT)
    print 'Get count with recv_type:', status.Get_count(recv_type)
    print 'Get elements with recv_type:', status.Get_elements(recv_type)
    print

    status = MPI.Status()
    comm.Recv([recv_buf, 1, recv_type], source=0, tag=2, status=status)
    print 'Get count with MPI.INT:', status.Get_count(MPI.INT)
    print 'Get elements with MPI.INT:', status.Get_elements(MPI.INT)
    print 'Get count with recv_type:', status.Get_count(recv_type)
    print 'Get elements with recv_type:', status.Get_elements(recv_type)

    recv_type.Free()