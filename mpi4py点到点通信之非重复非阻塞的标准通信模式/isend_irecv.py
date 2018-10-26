# isend_irecv.py

from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

send_obj = {'a': [1, 2.4, 'abc', -2.3+3.4J],
            'b': {2, 3, 4}}

if rank == 0:
    send_req = comm.isend(send_obj, dest=1, tag=11)
    send_req.wait()
    print 'process %d sends %s' % (rank, send_obj)
elif rank == 1:
    recv_req = comm.irecv(source=0, tag=11)
    recv_obj = recv_req.wait()
    print 'process %d receives %s' % (rank, recv_obj)