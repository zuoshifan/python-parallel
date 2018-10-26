# ssend_recv.py

from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

send_obj = {'a': [1, 2.4, 'abc', -2.3+3.4J],
            'b': {2, 3, 4}}

if rank == 0:
    comm.ssend(send_obj, dest=1, tag=11)
    print 'process %d sends %s' % (rank, send_obj)
elif rank == 1:
    recv_obj = comm.recv(source=0, tag=11)
    print 'process %d receives %s' % (rank, recv_obj)