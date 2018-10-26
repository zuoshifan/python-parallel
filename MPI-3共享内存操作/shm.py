# shm.py

"""
Demonstrates the usage of MPI-3 shared memory operation.

Run this with 4 processes like:
$ mpiexec -n 4 -host node1,node2 python shm.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# split the 4 processes into 2 sub-comms, each can share memory
shm_comm = comm.Split_type(MPI.COMM_TYPE_SHARED)
shm_rank = shm_comm.rank

itemsize = MPI.INT.Get_size()
if shm_rank == 0:
    nbytes = 10 * itemsize
else:
    nbytes = 0

# on rank 0 of shm_comm, create the contiguous shared block
win = MPI.Win.Allocate_shared(nbytes, itemsize, comm=shm_comm)

# create a numpy array whose data points to the shared mem
buf, itemsize = win.Shared_query(MPI.PROC_NULL)
# create a numpy array from buf
buf = np.array(buf, dtype='B', copy=False)
ary = np.ndarray(buffer=buf, dtype='i', shape=(10,))

# in process rank 1 of shm_comm:
# write the numbers 0, 1, 2, 3, 4 to the first 5 elements of the array
if shm_comm.rank == 1:
    ary[:5] = np.arange(5, dtype='i')

# wait in process rank 0 of shm_comm until process 1 has written to the array
shm_comm.Barrier()

# check that the array is actually shared and process 0 can see
# the changes made in the array by process 1 of shm_comm
if shm_comm.rank == 0:
    print ary


# show non-contiguous shared memory allocation
if shm_rank == 0:
    nbytes = 4 * itemsize
else:
    nbytes = 6 * itemsize

info = MPI.Info.Create()
info.Set('alloc_shared_noncontig', 'true')
win = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm, info=info)
info.Free()