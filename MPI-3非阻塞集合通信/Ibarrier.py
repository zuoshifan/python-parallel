# Ibarrier.py

"""
Demonstrates the usage of Ibarrier()

Run this with 4 processes like:
$ mpiexec -n 4 python Ibarrier.py
"""

import time
import random
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# synchronize here by blocking barrier
comm.Barrier()

# each process sleep for a random of time
time.sleep(random.random() / 100000)

# nonblocking barrier
req = comm.Ibarrier()

cnt = 0
while(not req.Test()):
    # do some work until all processes reach the Ibarrier
    print 'rank %d: %d' % (rank, cnt)
    cnt += 1

# do other things depend on this Ibarrier
# ...