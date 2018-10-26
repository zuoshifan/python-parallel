# multiproc.py
"""
"""

import numpy as np
import multiprocessing
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.rank

a = np.array([rank])

def worker(num):
    global a
    name = multiprocessing.current_process().name
    print 'Start %s' % name
    print 'rank %d: %s gets %d, %s' % (rank, name, num, a)
    a += 1
    print 'Exit %s' % name

proc1 = multiprocessing.Process(target=worker, args=(rank,))
if rank == 1:
    proc2 = multiprocessing.Process(target=worker, args=(rank,))

proc1.start()
if rank == 1:
    proc2.start()

proc1.join()
if rank == 1:
    proc2.join()

print  multiprocessing.current_process().name
print a


# import sys
# import numpy as np
# import multiprocessing
# from mpi4py import MPI


# comm = MPI.COMM_WORLD
# rank = comm.rank

# if rank == 0:
#     other = 1
# elif rank == 1:
#     other = 0
# else:
#     sys.exit(0)

# # initialize recv_buf to -1
# # recv_buf = np.array(-1)


# def send():
#     print '%s sends %d to rank %d...' % (multiprocessing.current_process().name, rank, other)
#     comm.Send(np.array(rank), dest=other, tag=11)

# def recv():
#     recv_buf = np.array(-1)
#     print '%s receives %d from rank %d' % (multiprocessing.current_process().name, rank, other)
#     # comm.Recv(recv_buf, source=other, tag=11)

# # create thread by using a function
# send_proc = multiprocessing.Process(target=send, name='[rank-%d send_proc]' % rank)
# recv_proc = multiprocessing.Process(target=recv, name='[rank-%d recv_proc]' % rank)

# # print 'before: rank %d has %d' % (rank, recv_buf)
# # start the threads
# send_proc.start()
# recv_proc.start()

# # wait for complete
# send_proc.join()
# recv_proc.join()
# # print 'after: rank %d has %d' % (rank, recv_buf)
