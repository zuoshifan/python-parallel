# spawn_slave1.py

"""
Demonstrates the usage of Get_parent, scatter, Disconnect.
"""

from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print 'slave1: rank %d of %d' % (rank, size)

recv_obj = comm.scatter([0, 1, 2], root=0)
print 'slave1: rank %d receives %d' % (rank, recv_obj)

# disconnect and free comm
MPI.Comm.Get_parent().Disconnect()
