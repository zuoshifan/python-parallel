# send_recv_timing.pu

import time
import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    data = np.random.randn(10000).astype(np.float64)
else:
    data = np.empty(10000, dtype=np.float64)

comm.barrier()

# use comm.send() and comm.recv()
t1 = time.time()
if rank == 0:
    comm.send(data, dest=1, tag=1)
else:
    comm.recv(source=0, tag=1)
t2 = time.time()
if rank == 0:
    print 'time used by send/recv: %f seconds' % (t2 - t1)

comm.barrier()

# use comm.Send() and comm.Recv()
t1 = time.time()
if rank == 0:
    comm.Send(data, dest=1, tag=2)
else:
    comm.Recv(data, source=0, tag=2)
t2 = time.time()
if rank == 0:
    print 'time used by Send/Recv: %f seconds' % (t2 - t1)