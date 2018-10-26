# Rsend_Recv_obj.py

import pickle
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

send_obj = {'a': [1, 2.4, 'abc', -2.3+3.4J],
            'b': {2, 3, 4}}

recv_buf = bytearray(2000) # pre-allocate a buffer for message receiving

if rank == 0:
    comm.Rsend(pickle.dumps(send_obj), dest=1, tag=11)
    print 'process %d sends %s' % (rank, send_obj)
elif rank == 1:
    comm.Recv(recv_buf, source=0, tag=11)
    print 'process %d receives %s' % (rank, pickle.loads(recv_buf))

    # or simply use comm.recv
    # recv_obj = comm.recv(source=0, tag=11)
    # print 'process %d receives %s' % (rank, recv_obj)