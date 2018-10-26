# trick5.py

"""
Make the script work both with and without mpi4py.

Run this with 4 processes like:
$ mpiexec -n 4 python trick5.py
or
$ python trick5.py
"""

import mpiutil3

rank = mpiutil3.rank
size = mpiutil3.size

# compute pi/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - 1/11 + ...
N_max = 10000
local_num = N_max / size
local_sum = 0.0
for i in range(rank*local_num, (rank + 1)*local_num):
    local_sum += (-1)**i * 1.0 / (2*i + 1)

# reduce
sum_ = mpiutil3.reduce(local_sum, root=0, op=mpiutil3.SUM)

if rank == 0:
    pi = 4.0 * sum_
    print 'pi =', pi
