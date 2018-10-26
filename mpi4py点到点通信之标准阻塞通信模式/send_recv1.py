# send_recv1.py

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

send_obj = np.arange(10, dtype='i')
recv_buf = bytearray(2000)

if rank == 0:
    comm.send(send_obj, dest=1, tag=11)
    recv_obj = comm.recv(recv_buf,source=1, tag=22)
    import pickle
    # print recv_buf
    print pickle.loads(recv_buf)
elif rank == 1:
    recv_obj = comm.recv(source=0, tag=11)
    comm.send(send_obj, dest=0, tag=22)

print 'process %d receives %s' % (rank, recv_obj)


# import pickle
# import numpy as np
# from mpi4py import MPI

# comm = MPI.COMM_WORLD
# size = comm.Get_size()
# rank = comm.Get_rank()

# in_data = np.array([rank], dtype=np.double)
# comm.send(in_data, ((rank+1) % size))

# out_data = bytearray(200)
# comm.recv(out_data, source=(rank-1) % size)

# print 'node %s: received %s' % (rank, pickle.loads(out_data))