# trick4.py

"""
Use a new communicator.

Run this with 5 processes like:
$ mpiexec -n 5 python trick4.py
"""

import mpiutil2

rank = mpiutil2.rank
size = mpiutil2.size

# compute pi/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - 1/11 + ...
N_max = 10000
local_num = N_max / size
local_sum = 0.0
for i in range(rank*local_num, (rank + 1)*local_num):
    local_sum += (-1)**i * 1.0 / (2*i + 1)

if size >= 5:
    comm = mpiutil2.comm
    # create a new communicator by including rank 0, 1, 2, 3 only
    new_comm = comm.Create(comm.Get_group().Incl([0, 1, 2, 3]))
    if rank <= 3:
        print 'use new comm with size: %d' % new_comm.size

        # reduce
        sum_ = mpiutil2.reduce(local_sum, root=0, comm=new_comm)

        if rank == 0:
            pi = 4.0 * sum_
            print 'pi =', pi
