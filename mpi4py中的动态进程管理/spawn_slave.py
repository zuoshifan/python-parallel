# spawn_slave.py

"""
Demonstrates the usage of Get_parent, Scatter, Gather, Disconnect.
"""

import numpy as np
from mpi4py import MPI

# get the parent intercommunicator
comm = MPI.Comm.Get_parent()
print 'slave: rank %d of %d' % (comm.rank, comm.size)

# receive data from master process
recv_buf = np.array(0, dtype='i')
comm.Scatter(None, recv_buf, root=0)
print 'slave: rank %d receives %d' % (comm.rank, recv_buf)

# increment the received data
recv_buf += 1

# send the incremented data to master
comm.Gather(recv_buf, None, root=0)
print 'slave: rank %d sends %d' % (comm.rank, recv_buf)

# disconnect and free comm
comm.Disconnect()