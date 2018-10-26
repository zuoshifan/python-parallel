# barrier.py

"""
Demonstrates the usage of barrier, Barrier.

Run this with 2 processes like:
$ mpiexec -n 2 python barrier.py
"""

import os
import shutil
import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# ---------------------------------------------------------------------
# example 1
count = 10
send_buf = np.arange(count, dtype='i')
recv_buf = np.empty(count, dtype='i')

if rank == 0:
    comm.Rsend(send_buf, dest=1, tag=11)
    comm.Barrier() # synchronization here
    print 'process %d sends %s' % (rank, send_buf)
elif rank == 1:
    comm.Barrier() # synchronization here
    comm.Recv(recv_buf, source=0, tag=11)
    print 'process %d receives %s' % (rank, recv_buf)


# ---------------------------------------------------------------------
# example 2
temp_dir = './temp_dir'
temp_file = 'temp_file%d.txt' % rank
# rank 0 crates the directory first if necessary
if not os.path.isdir(temp_dir):
    if rank == 0:
        os.mkdir(temp_dir)
        print 'rank %d creates dir: %s' % (rank, temp_dir)

# synchronization before writing to temp_dir
comm.Barrier()

# each process creates its own file
open(temp_dir + '/' + temp_file, 'w').close()
print 'rank %d creates file: %s' % (rank, temp_dir + '/' + temp_file)

# synchronization before remove temp_dir
comm.Barrier()

# now remove temp_dir by rank 0
if rank == 0:
    shutil.rmtree(temp_dir)
    print 'rank %d removes dir: %s' % (rank, temp_dir)