# scatter.py

from mpi4py import MPI


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    data = [ (i + 1)**2 for i in range(size) ]
    print 'before scattering: process %d has %s' % (rank, data)
else:
    data = None
    print 'before scattering: process %d has %s' % (rank, data)

data = comm.scatter(data, root=0)
print 'after scattering: process %d has %s' % (rank, data)