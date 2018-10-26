# hello.pyx

from cython import parallel
from mpi4py import MPI


# function that uses MPI and OpenMP hybrid programming
def say_hello(comm):
    cdef unsigned int thread_id
    cdef int i

    # use 2 OpenMP threads to execute the following code
    with nogil, parallel.parallel(num_threads=2):
        # allocate 3 tasks to the 2 threads with a chunk size of 2
        # and a static schedule, so thread 0 will have task 0 and 1,
        # thread 1 will have task 2
        for i in parallel.prange(3, schedule="static", chunksize=2):
            # get the thread id
            thread_id = parallel.threadid()
            # acquire the GIL for Python operation like print
            with gil:
                # get the rank of the MPI process
                rank = comm.rank
                # get the processor name
                pname = MPI.Get_processor_name()
                print 'MPI rank %d, OpenMP thread %d in %s says hello' % (rank, thread_id, pname)