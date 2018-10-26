# gather.py

from mpi4py import MPI


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

data = (rank + 1)**2
print 'before gathering: process %d has %s' % (rank, data)

data = comm.gather(data, root=0)
print 'after scattering: process %d has %s' % (rank, data)