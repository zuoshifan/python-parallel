# mpi3_rma.py

"""
Demonstrates the usage of MPI-3 enhanced RMA.

Run this with 4 processes like:
$ mpiexec -n 4 python mpi3_rma.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Create
if rank == 0:
    win = MPI.Win.Create(None, comm=comm)

    # Lock_all
    win.Lock_all()
    for rk in [1, 2, 3]:
        a = np.array([rk, rk], dtype='i')
        # Put
        win.Put(a, target_rank=rk)
        print 'rank %d put %s to rank %d' % (rank, a, rk)
    # Unlock_all
    win.Unlock_all()

    # Lock for rank 1
    win.Lock(rank=1)
    b = np.array([10, 10], dtype='i')
    c = np.array([-1, -1], dtype='i')
    # Get_accumulate
    win.Get_accumulate(b, c, target_rank=1, op=MPI.SUM)
    # Unlock for rank 1
    win.Unlock(rank=1)
    print 'rank %d Get_accumulate %s to rank 1, and get result %s' % (rank, b, c)

    comm.Barrier()
else:
    mem = np.array([-1, -1], dtype='i')
    win = MPI.Win.Create(mem, comm=comm)
    comm.Barrier()

    print 'rank %d get %s' % (rank, mem)


# Allocate
if rank == 0:
    win = MPI.Win.Allocate(0, disp_unit=4, comm=comm)
    # Lock_all
    win.Lock_all()
    reqs = []
    for rk in [1, 2, 3]:
        a = np.array([rk, rk], dtype='i')
        # Rput
        req = win.Rput(a, target_rank=rk)
        reqs.append(req)
        print 'rank %d put %s to rank %d' % (rank, a, rk)
    # compute all Rput
    MPI.Request.Waitall(reqs)
    # Unlock_all
    win.Unlock_all()
    comm.Barrier()
else:
    win = MPI.Win.Allocate(8, disp_unit=4, comm=comm)
    comm.Barrier()
    # convert the memory of win to numpy array
    buf = np.array(buffer(win.tomemory()), dtype='B', copy=False)
    mem = np.ndarray(buffer=buf, dtype='i', shape=(2,))

    print 'rank %d get %s' % (rank, mem)


# Create_dynamic
win = MPI.Win.Create_dynamic(comm=comm)
mem = MPI.Alloc_mem(8)
# Attach and Detach
win.Attach(mem)
win.Detach(mem)
MPI.Free_mem(mem)