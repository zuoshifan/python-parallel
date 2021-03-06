# mpiutil2.py

"""Utilities for making MPI usage transparent."""

import warnings


rank = 0
size = 1
comm = None

## try to setup MPI and get the comm, rank and size
## if not they should end up as comm = None, rank=0, size=1
try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD

    rank = comm.Get_rank()
    size = comm.Get_size()

except ImportError:
    warnings.warn("Warning: mpi4py not installed.")


def reduce(sendobj, root=0, op=None, comm=comm):
    if comm is not None and comm.size > 1:
        return comm.reduce(sendobj, root=root, op=(op or MPI.SUM))
    else:
        return sendobj
