import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD

# create a shared array of size 1000 elements of type double
size = 10
itemsize = MPI.DOUBLE.Get_size()
if comm.Get_rank() == 0:
    # nbytes = size * itemsize
    nbytes = 4 * itemsize
else:
    # nbytes = 0
    nbytes = 3 * itemsize
# nbytes = 2 * itemsize

info = MPI.Info.Create()
info.Set('alloc_shared_noncontig', 'true')
# on rank 0, create the shared block
# on rank 1 get a handle to it (known as a window in MPI speak)
# win = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm, info=info)
win = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm)
# mem = win.tomemory()
# print 'rank %d: %s' % (comm.rank, mem.address)
# buffer(mem)[:] = 0
# print memoryview(mem)[:]
# if comm.rank == 0:
#     for i in range(5*itemsize):
#         print mem[i]
# # print 'rank %d: %s, %s' % (comm.rank, mem.nbytes, mem.address)
# addrs = comm.gather(mem.address, root=0)
# if comm.rank == 0:
#     print np.diff(addrs)
info.Free()

arys = []
for i in range(comm.size):
    buf, itemsize = win.Shared_query(i)
    buf = np.array(buf, dtype='B', copy=False)
    arys.append(np.ndarray(buffer=buf, dtype='d', shape=(len(buf)/itemsize,)))

arys[comm.rank][:] = comm.rank
comm.barrier()

print arys[0]
print arys[1]
print arys[2]

# # create a numpy array whose data points to the shared mem
# buf, itemsize = win.Shared_query(0)
# print 'rank %d: %s' % (comm.rank, buf.address)
# print buf.address
# print 'rank %d: %s, %s' % (comm.rank, mem.nbytes, buf.nbytes)
# buf, itemsize = win.Shared_query(MPI.PROC_NULL)
# if comm.rank == 0:
#     addrs = []
#     buf, itemsize = win.Shared_query(MPI.PROC_NULL)
#     print 'rank %d: %s, %s' % (comm.rank, buf.nbytes, buf.address)
#     for i in range(comm.size):
#         buf, itemsize = win.Shared_query(i)
#         print 'rank %d: %s, %s' % (comm.rank, buf.nbytes, buf.address)
#         addrs.append(buf.address)
#     print np.diff(addrs)

# # assert itemsize == MPI.DOUBLE.Get_size()
# buf = np.array(buf, dtype='B', copy=False)
# ary = np.ndarray(buffer=buf, dtype='d', shape=(size,))

# # in process rank 1:
# # write the numbers 0.0,1.0,..,4.0 to the first 5 elements of the array
# if comm.rank == 1:
#     ary[:5] = np.arange(5)

# # wait in process rank 0 until process 1 has written to the array
# comm.Barrier()

# # check that the array is actually shared and process 0 can see
# # the changes made in the array by process 1
# if comm.rank == 0:
#     print(ary[:10])