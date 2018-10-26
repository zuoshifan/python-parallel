from cython.parallel import parallel, prange, threadid
from libc.stdlib cimport abort, malloc, free


cdef Py_ssize_t idx, i, j, n = 3
cdef int * local_buf
cdef size_t size = 10
cdef unsigned int thread_id

# cdef func(int* x) nogil:
#     x[0] += 1
#     # cdef Py_ssize_t i

#     # for i in prange(x.shape[0]):
#     #     x[i] = 2 * x[i]


# with nogil, parallel():
with nogil, parallel(num_threads=4):
    local_buf = <int *> malloc(sizeof(int) * size)
    if local_buf is NULL:
        abort()

    # populate our local buffer in a sequential loop
    thread_id = threadid()
    for i in xrange(size):
        # local_buf[i] = i * 2
        local_buf[i] = thread_id

    # # share the work using the thread-local buffer(s)
    for j in prange(n, schedule='guided'):
        # func(local_buf)
        with gil:
            print '%d : %d, %d' % (j, threadid(), local_buf[0])
        local_buf[0] = local_buf[0] + 1

    with gil:
        print '%d : %d' % (threadid(), local_buf[0])

    free(local_buf)


#--------------------------------------------------------------------------

# from cython.parallel import prange
# cimport openmp

# cdef int i
# cdef int n = 3
# cdef int sum = 0
# cdef int num_threads

# for i in prange(n, nogil=True):
#     # sum += i
#     num_threads = openmp.omp_get_num_threads()
#     sum += num_threads

# print(sum)


#--------------------------------------------------------------------------

# from cython import parallel


# def do_without_gil():
#     cdef:
#       unsigned int thread_id
#       int i
#     with nogil, parallel.parallel(num_threads=2):
#         for i in parallel.prange(3, schedule="static", chunksize=2):
#             thread_id = parallel.threadid()
#             with gil:
#                 print '%d : %d' % (i, thread_id)
