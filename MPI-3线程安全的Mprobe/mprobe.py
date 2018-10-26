# mprobe.py

"""
Demonstrates the usage of mprobe.

Run this with 2 processes like:
$ mpiexec -n 2 python mprobe.py
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

# -----------------------------------------------------------------------------------
# mprobe and recv
if rank == 0:
    comm.send(11, dest=1, tag=11)
    comm.send(22, dest=1, tag=22)
elif rank == 1:

    def recv():

        status = MPI.Status()
        msg = comm.mprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        # msg = MPI.Message.probe(comm, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)

        recv_obj = msg.recv()
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


comm.barrier()

# ------------------------------------------------------------------------------------
# Mprobe and Recv
if rank == 0:
    comm.Send(np.array([33, 33]), dest=1, tag=33)
    comm.Send(np.array([44, 44]), dest=1, tag=44)
elif rank == 1:

    def recv():

        status = MPI.Status()
        msg = comm.Mprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        # msg = MPI.Message.Probe(comm, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)

        recv_buf = np.array([-1, -1])
        msg.Recv(recv_buf)
        print '%s receives %s from rank 0' % (threading.currentThread().getName(), recv_buf)

    # create thread by using a function
    recv_thread1 = threading.Thread(target=recv, name='[rank-%d recv_thread 1]' % rank)
    recv_thread2 = threading.Thread(target=recv, name='[rank-%d recv_thread 2]' % rank)

    # start the threads
    recv_thread1.start()
    recv_thread2.start()

    # wait for complete
    recv_thread1.join()
    recv_thread2.join()


comm.barrier()

# ------------------------------------------------------------------------------------
# improbe and irecv
if rank == 0:
    comm.send(55, dest=1, tag=55)
    comm.send(66, dest=1, tag=66)
elif rank == 1:

    def recv():

        status = MPI.Status()
        msg = None
        while not msg:
            msg = comm.improbe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            # msg = MPI.Message.iprobe(comm, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            if msg is None:
                print '%s improbe is not completed...' % threading.currentThread().getName()

        req = msg.irecv()
        recv_obj = req.wait()
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


comm.barrier()

# ------------------------------------------------------------------------------------
# Improbe and Irecv
if rank == 0:
    comm.Send(np.array([77, 77]), dest=1, tag=77)
    comm.Send(np.array([88, 88]), dest=1, tag=88)
elif rank == 1:

    def recv():

        status = MPI.Status()
        msg = None
        while not msg:
            msg = comm.Improbe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            # msg = MPI.Message.Iprobe(comm, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            if msg is None:
                print '%s Improbe is not completed...' % threading.currentThread().getName()

        recv_buf = np.array([-1, -1])
        req = msg.Irecv(recv_buf)
        req.Wait()
        print '%s receives %s from rank 0' % (threading.currentThread().getName(), recv_buf)

    # create thread by using a function
    recv_thread1 = threading.Thread(target=recv, name='[rank-%d recv_thread 1]' % rank)
    recv_thread2 = threading.Thread(target=recv, name='[rank-%d recv_thread 2]' % rank)

    # start the threads
    recv_thread1.start()
    recv_thread2.start()

    # wait for complete
    recv_thread1.join()
    recv_thread2.join()
