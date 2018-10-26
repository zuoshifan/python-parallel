# Idup.py

"""
Demonstrates the usage of Idup and Create_group.

Run this with 4 processes like:
$ mpiexec -n 4 python Idup.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Idup
comm_dup, req = comm.Idup()
req.Wait()
recv_obj = comm_dup.scatter([1, 2, 3, 4], root=0)
print 'rank %d has %d' % (rank, recv_obj)

# make one process die
if rank == 0:
    # process 0 dies
    exit()
# other processes can still work

# Create_group
# sub_comm = comm.Create(comm.group.Excl([0])) # dead lock for Create
sub_comm1 = comm.Create_group(comm.group.Excl([0])) # OK for Create_group

print 'sub_comm1.rank %d   <->   comm.rank %d' % (sub_comm1.rank, rank)

sub_comm2 = comm.Create_group(comm.group.Excl([0, 1])) # OK for Create_group
if rank >=2:
    print 'sub_comm2.rank %d   <->   comm.rank %d' % (sub_comm2.rank, rank)
else:
    print sub_comm2 == MPI.COMM_NULL

sub_comm3 = comm.Create_group(MPI.GROUP_NULL) # OK for Create_group
print sub_comm3 == MPI.COMM_NULL