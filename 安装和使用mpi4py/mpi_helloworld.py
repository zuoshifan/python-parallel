# mpi_helloworld.py

from mpi4py import MPI


# # get MPI version number
# version = MPI.Get_version()
# print version

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
node_name = MPI.Get_processor_name() # get the name of the node

print 'Hello world from process %d at %s.' % (rank, node_name)