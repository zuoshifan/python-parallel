# pack.py

"""
Demonstrates the usage of Pack, Unpack, Pack_size.

Run this with 2 processes like:
$ mpiexec -n 2 python pack.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# get pack size of some data type
print 'pack size of 3 MPI.INT:', MPI.INT.Pack_size(3, comm)
print 'pack size of 3 MPI.DOUBLE:', MPI.DOUBLE.Pack_size(3, comm)

# --------------------------------------------------------------------------------
# demonstrate Pack and Unpack
buf_size = 100
pack_buf = bytearray(buf_size)

a = np.array([1, 2], dtype='i') # two int type
b = np.array(0.5, dtype='f8') # a double type
# or
# b = np.array([0.5], dtype='f8') # a double type

# pack two int and a double into pack_buf
position = 0
position = MPI.INT.Pack(a, pack_buf, position, comm) # position = 4 * 2
position = MPI.DOUBLE.Pack(b, pack_buf, position, comm) # position = 4 * 2 + 8

a1 = np.array([0, 0], dtype='i') # two int type with initial value 0
b1 = np.array(0.0, dtype='f8') # a double type with initial value 0.0

# unpack two int and a double from pack_buf to a1, b1
position = 0
position = MPI.INT.Unpack(pack_buf, position, a1, comm) # position = 4 * 2
position = MPI.DOUBLE.Unpack(pack_buf, position, b1, comm) # position = 4 * 2 + 8
print 'a1 = [%d, %d], b1 = %f' % (a1[0], a1[1], b1)

# --------------------------------------------------------------------------------
# demonstrate how to send and receive a packed buffer
new_pack_buf = bytearray(buf_size)
if rank == 0:
    a = np.array(1, dtype='i') # an int type
    b = np.array(0.5, dtype='f8') # a double type
    # pack an int and a double into pack_buf
    packsize = 0
    packsize = MPI.INT.Pack(a, pack_buf, packsize, comm) # packsize = 4
    packsize = MPI.DOUBLE.Pack(b, pack_buf, packsize, comm) # packsize = 4 + 8
    # first send packsize to rank 1, it will use it to receive the packed data
    comm.send(packsize, dest=1, tag=11)
    # then send the packed data to rank 1
    comm.Send([pack_buf, packsize, MPI.PACKED], dest=1, tag=22)
    print 'rank 0 send: a = %d, b = %f' % (a, b)
elif rank == 1:
    a = np.array(0, dtype='i') # an int type with initial value 0
    b = np.array(0.0, dtype='f8') # a double type with initial value 0.0
    # receive packsize from rank 0
    packsize = comm.recv(source=0, tag=11)
    # use packsize to receive the packed data from rank 0
    comm.Recv([pack_buf, packsize, MPI.PACKED], source=0, tag=22)
    # unpack an int and a double from pack_buf to a, b
    position = 0
    position = MPI.INT.Unpack(pack_buf, position, a, comm) # position = 4
    position = MPI.DOUBLE.Unpack(pack_buf, position, b, comm) # position = 4 + 8
    print 'rank 1 receives: a = %d, b = %f' % (a, b)