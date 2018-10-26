# bcast.py

from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    data = {'key1' : [7, 2.72, 2+3j],
            'key2' : ( 'abc', 'xyz')}
    print 'before broadcasting: process %d has %s' % (rank, data)
else:
    data = None
    print 'before broadcasting: process %d has %s' % (rank, data)

data = comm.bcast(data, root=0)
print 'after broadcasting: process %d has %s' % (rank, data)