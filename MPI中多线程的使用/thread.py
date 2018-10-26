# thread.py

"""
Demonstrates the usage of threads with MPI.

Run this with 2 processes like:
$ mpiexec -n 2 python thread.py
"""


import sys
import numpy as np
import threading
from mpi4py import MPI


if MPI.Query_thread() < MPI.THREAD_MULTIPLE:
    sys.stderr.write("MPI does not provide enough thread support\n")
    sys.exit(0)

comm = MPI.COMM_WORLD
rank = comm.rank

if rank == 0:
    other = 1
elif rank == 1:
    other = 0
else:
    sys.exit(0)

# initialize recv_buf to -1
recv_buf = np.array(-1)


def send():
    current_thread = threading.currentThread()
    print '%s is main thread: %s' % (current_thread.name, MPI.Is_thread_main())
    print '%s sends %d to rank %d...' % (current_thread.name, rank, other)
    comm.Send(np.array(rank), dest=other, tag=11)

def recv():
    current_thread = threading.currentThread()
    print '%s is main thread: %s' % (current_thread.name, MPI.Is_thread_main())
    comm.Recv(recv_buf, source=other, tag=11)
    print '%s receives %d from rank %d' % (current_thread.name, recv_buf, other)

# create thread by using a function
send_thread = threading.Thread(target=send, name='[rank-%d send_thread]' % rank)
recv_thread = threading.Thread(target=recv, name='[rank-%d recv_thread]' % rank)

current_thread = threading.currentThread()
print '%s is main thread: %s' % (current_thread.name, MPI.Is_thread_main())
print 'before: rank %d has %d' % (rank, recv_buf)
# start the threads
send_thread.start()
recv_thread.start()

# wait for terminate
send_thread.join()
recv_thread.join()
print 'after: rank %d has %d' % (rank, recv_buf)