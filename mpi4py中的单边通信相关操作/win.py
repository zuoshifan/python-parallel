# win.py

"""
Demonstrates the usage of Create, Free, Put, Get, Accumulate.

Run this with 4 processes like:
$ mpiexec -n 4 python win.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Create and Put
if rank == 0:
    mem = np.array([1, 2], dtype='i')
    # create a window object with no accessable memory, used to communicate with other only
    win =  MPI.Win.Create(None, comm=comm)
    # synchronize
    win.Fence()
    # put data into a memory window of rank 1
    print 'rank 0 puts %s to rank 1' % mem
    win.Put(mem, target_rank=1)
    # synchronize
    win.Fence()
else:
    # initialize a memory of [0, 0]
    mem = np.array([0, 0], dtype='i')
    # use mem to create a window for receiving data
    win =  MPI.Win.Create(mem, comm=comm)
    # synchronize
    win.Fence()
    # synchronize
    win.Fence()
    print 'rank %d has %s after put' % (rank, mem)


# Get and Accumulate
if rank == 0:
    a = np.array(0.5, dtype='d')
    # initialize acc with 0.0
    acc = np.array(0.0, dtype='d')
    # create window objects
    win_a =  MPI.Win.Create(a, comm=comm)
    win_acc =  MPI.Win.Create(acc, comm=comm)
    # synchronize for win_a
    win_a.Fence()
    # synchronize for win_a
    win_a.Fence()
    # synchronize for win_acc
    win_acc.Fence()
    # synchronize for win_acc
    win_acc.Fence()
    # after accumulate, print the value of acc = 0.5 + 0.5 + 0.5
    print 'rank 0 has acc = %s' % acc
else:
    # initialize a with 0.0
    a = np.array(0.0, dtype='d')
    win_a =  MPI.Win.Create(None, comm=comm)
    win_acc =  MPI.Win.Create(None, comm=comm)
    # synchronize for win_a
    win_a.Fence()
    # get data from a memory window of rank 0
    win_a.Get(a, target_rank=0)
    # synchronize for win_a
    win_a.Fence()
    print 'rank %d has a = %s' % (rank, a)
    # synchronize for win_acc
    win_acc.Fence()
    # each rank except 0 accumulates a to the memory window of rank 0
    win_acc.Accumulate(a, target_rank=0, op=MPI.SUM)
    # synchronize for win_acc
    win_acc.Fence()

# free the window object
win.Free()
win_a.Free()
win_acc.Free()