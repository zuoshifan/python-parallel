# probe_error.py

"""
This is an example which shows the incorrect use of probe in
multi-threading environment.

Run this with 2 processes like:
$ mpiexec -n 2 python probe_error.py
"""

import sys
import time
import numpy as np
import threading
from mpi4py import MPI


if MPI.Query_thread() < MPI.THREAD_MULTIPLE:
    sys.stderr.write("MPI does not provide enough thread support\n")
    sys.exit(0)

comm = MPI.COMM_WORLD
rank = comm.rank

# -----------------------------------------------------------------------------------
# mprobe and recv
if rank == 0:
    comm.send(11, dest=1, tag=11)
    comm.send(22, dest=1, tag=22)
elif rank == 1:

    def recv():

        status = MPI.Status()
        comm.probe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        print '%s probed source = %d, tag = %d' % (threading.currentThread().getName(), status.source, status.tag)

        time.sleep(0.5)

        recv_obj = comm.recv(source=status.source, tag=status.tag)
        print '%s receives %d from rank 0' % (threading.currentThread().getName(), recv_obj)

    # create thread by using a function
    recv_thread1 = threading.Thread(target=recv, name='[rank-%d recv_thread 1]' % rank)
    recv_thread2 = threading.Thread(target=recv, name='[rank-%d recv_thread 2]' % rank)

    # start the threads
    recv_thread1.start()
    recv_thread2.start()

    # wait for complete
    recv_thread1.join()
    recv_thread2.join()
