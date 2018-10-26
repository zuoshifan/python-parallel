# trick1.py

"""
Make the script work both with and without mpi4py.

Run this with 4 processes like:
$ mpiexec -n 4 python trick1.py
or
$ python trick1.py
"""

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


# compute pi/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - 1/11 + ...
N_max = 10000
local_num = N_max / size
local_sum = 0.0
for i in range(rank*local_num, (rank + 1)*local_num):
    local_sum += (-1)**i * 1.0 / (2*i + 1)

# reduce
if comm is None:
# if size == 1:
    pi = 4.0 * local_sum
else:
    sum_ = comm.reduce(local_sum, root=0, op=MPI.SUM)
    if rank == 0:
        pi = 4.0 * sum_

if rank == 0:
    print 'pi =', pi
