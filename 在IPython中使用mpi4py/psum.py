# psum.py

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD

def psum(a):
    # locsum = np.sum(a)
    locsum = np.array(np.sum(a))
    rcvBuf = np.array(0.0, 'd')
    comm.Allreduce([locsum, MPI.DOUBLE], [rcvBuf, MPI.DOUBLE], op=MPI.SUM)

    return rcvBuf