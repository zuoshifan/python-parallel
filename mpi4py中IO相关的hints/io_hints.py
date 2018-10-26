# io_hints.py

"""
Demonstrates how to pass I/O related hints to the implementation.

Run this with 4 processes like:
$ mpiexec -n 4 python io_hints.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

buf = np.full((5,), rank, dtype='i')

filename = 'temp.txt'

# create a MPI.Info object
info = MPI.Info.Create()
# set some MPI predefined hints
# number of I/O devices across which the file should be striped
info['striping_factor'] = '16'
# the striping unit in bytes
info['striping_unit'] = '1048576'
# buffer size for collective I/O
info['cb_buffer_size'] = '8388608'
# number of processes that should perform disk accesses during collective I/O
info['cb_nodes'] = '%d' % comm.size
# set some additional hints supported by ROMIO
# buffer size for data sieving in independent reads
info['ind_rd_buffer_size'] = '2097152'
# buffer size for data sieving in independent writes
info['ind_wr_buffer_size'] = '1048576'

# open the file for read and write, create it if it does not exist,
# and delete it on close, with the info object defined above
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE, info=info)

# free the info object
info.Free()

# get the currently used hints
info_used = fh.Get_info()
if rank == 0:
    for k in info_used:
        print '%s: %s' % (k, info_used[k])

# close the file
fh.Close()