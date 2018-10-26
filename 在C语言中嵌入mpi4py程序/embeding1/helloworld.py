# helloworld.py

from mpi4py import MPI


hwmess = 'Hello, World! I am process %d of %d on %s.'
myrank = MPI.COMM_WORLD.Get_rank()
nprocs = MPI.COMM_WORLD.Get_size()
procnm = MPI.Get_processor_name()
print (hwmess % (myrank, nprocs, procnm))
