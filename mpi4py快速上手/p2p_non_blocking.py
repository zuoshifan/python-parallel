# p2p_non_blocking.py

from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    data = {'a': 7, 'b': 3.14}
    print 'process %d sends %s' % (rank, data)
    req = comm.isend(data, dest=1, tag=11)
    req.wait()
elif rank == 1:
    req = comm.irecv(source=0, tag=11)
    data = req.wait()
    print 'process %d receives %s' % (rank, data)