# Aint_add_diff.py


"""
Demonstrates the usage of MPI.Aint_add and MPI.Aint_diff.

Run this with 2 processes like:
$ mpiexec -n 2 python Aint_add_diff.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.rank

ary = np.arange(10, dtype='i')
base = MPI.Get_address(ary)
print 'rank %d has base address: %d' % (rank, base)
disp = 4
addr = MPI.Aint_add(base, disp)
print 'rank %d has base + %d = %d' % (rank, disp, addr)
diff = MPI.Aint_diff(addr, base)
print 'rank %d has %d - base = %d' % (rank, addr, diff)