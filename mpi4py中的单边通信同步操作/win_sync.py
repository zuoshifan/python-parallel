# win_sync.py

"""
Demonstrates the usage of Start, Complete, Post, Wait, Lock, Unlock.

Run this with 2 processes like:
$ mpiexec -n 2 python win.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

SIZE1 = 5
SIZE2 = 10

if rank == 0:
    A = np.zeros(SIZE2, dtype='i') # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    win =  MPI.Win.Create(None, comm=comm)
    # create a group with rank 1 only
    grp = comm.group.Incl(ranks=[1])

    # start remote memory access
    win.Start(grp)
    # put the first 5 elements of A of rank 0 to A[:5] of rank 1
    win.Put(A[:SIZE1], target_rank=1)
    # end remote memory access
    win.Complete()

    # lock to protect the get operation
    win.Lock(rank=1, lock_type=MPI.LOCK_SHARED)
    # get last 5 elements of A of rank 1 to A[:5] of rank 0
    win.Get(A[:SIZE1], target_rank=1, target=[5*4, 5, MPI.INT])
    # unlock after the get operation
    win.Unlock(rank=1)
    print 'rank 0 has A = %s' % A
else:
    A = np.zeros(SIZE2, dtype='i') + 1 # [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    win =  MPI.Win.Create(A, comm=comm)
    # create a group with rank 0 only
    grp = comm.group.Incl(ranks=[0])

    # start remote memory access
    win.Post(grp)
    # end remote memory access
    win.Wait()

    # no need for Lock and Unlock here

    print 'rank 1 has A = %s' % A
