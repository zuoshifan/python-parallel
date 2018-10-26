# spawn_master.py

"""
Demonstrates the usage of Spawn, Scatter, Gather, Disconnect.

Run this with 1 process like:
$ mpiexec -n 1 python spawn_master.py
# or
$ python spawn_master.py
"""

import sys
import numpy as np
from mpi4py import MPI

# create two new processes to execute spawn_slave.py
comm = MPI.COMM_SELF.Spawn(sys.executable, ['spawn_slave.py'], maxprocs=2)
print 'master: rank %d of %d' % (comm.rank, comm.size)

# scatter [1, 2] to the two new processes
send_buf = np.array([1, 2], dtype='i')
comm.Scatter(send_buf, None, root=MPI.ROOT)
print 'master: rank %d sends %s' % (comm.rank, send_buf)

# gather data from the two new processes
recv_buf = np.array([0, 0], dtype='i')
comm.Gather(None, recv_buf, root=MPI.ROOT)
print 'master: rank %d receives %s' % (comm.rank, recv_buf)

# disconnect and free comm
comm.Disconnect()