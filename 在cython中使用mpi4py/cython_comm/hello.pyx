# hello.pyx

# python level
from mpi4py import MPI

def say_hello(comm):
    rank = comm.rank
    print 'say_hello: Hello from rank = %d' % rank


# ----------------------------------------------------------------------------
# cython and C level
from mpi4py cimport MPI
from mpi4py cimport libmpi as mpi

def c_say_hello(MPI.Comm comm):
    # get the C handle of MPI.Comm
    cdef mpi.MPI_Comm c_comm = comm.ob_mpi
    cdef int ierr=0
    cdef int rank = 0
    # call MPI C API to get rank
    ierr = mpi.MPI_Comm_rank(c_comm, &rank)
    print 'c_say_hello: Hello from rank = %d' % rank

def return_comm(MPI.Comm comm):
    # get the C handle of MPI.Comm
    cdef mpi.MPI_Comm c_comm = comm.ob_mpi
    cdef mpi.MPI_Group c_group
    # call MPI C API to get the associated group of c_comm
    mpi.MPI_Comm_group(c_comm, &c_group)
    cdef int n = 1
    cdef int *ranks = [0]
    cdef mpi.MPI_Group c_new_group
    # call MPI C API to create a new group by excluding rank 0
    mpi.MPI_Group_excl(c_group, n, ranks, &c_new_group)
    cdef mpi.MPI_Comm c_new_comm
    # call MPI C API to create a new communicator by excluding rank 0
    mpi.MPI_Comm_create(c_comm, c_new_group, &c_new_comm)

    cdef MPI.Comm py_comm
    if comm.rank == 0:
        return None
    else:
        # initialize a MPI.Comm object
        py_comm = MPI.Comm()
        # assign the new communicator to py_comm.ob_mpi
        py_comm.ob_mpi = c_new_comm

        return py_comm
