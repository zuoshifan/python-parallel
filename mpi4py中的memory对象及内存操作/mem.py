# mem.py

"""
Demonstrates memory operations.

Run this with 1 processes like:
$ mpiexec -n 1 python mem.py
or
$ python mem.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.rank

# create a MPI.memory object from a byte string
mem = MPI.memory.frombuffer(b"abc", readonly=True)
print 'mem.address:', mem.address
print 'mem.nbytes:', mem.nbytes
print 'mem.readonly:', mem.readonly
# get the read-only buffer of mem
buf = buffer(mem)
print 'buffer:', buf
# create a memory view of mem
mv = memoryview(mem)
print 'mv[0]:', mv[0]
try:
    # try to modify a readonly buffer
    mv[0] = 'x'
except TypeError as e:
    print e
# release the memory object
mem.release()

print

# create a MPI.memory object from a byte array, which stands for ASCII code a, b, c
mem = MPI.memory.frombuffer(bytearray([97, 98, 99]), readonly=False)
addr = mem.address
nbytes = mem.nbytes
# create a new MPI.memory object which shares the memory of mem
mem1 = MPI.memory.fromaddress(addr, nbytes, readonly=False)
# get the read-only buffer of mem
buf = buffer(mem)
print 'buffer:', buf
try:
    # try to change the read-only buffer object
    buf[0] = b'x'
except TypeError as e:
    print e
# create a memory view of mem
mv = memoryview(mem)
# create a memory view of mem1
mv1 = memoryview(mem1)
print 'before change: mv[0] = %s, mv1[0] = %s' % (mv[0], mv1[0])
# change mv[0]
mv[0] = 'x'
print 'after change: mv[0] = %s, mv1[0] = %s' % (mv[0], mv1[0])
# release the memory object
mem.release()

print

# allocate a memory of 40 bytes, return a MPI.memory object
mem = MPI.Alloc_mem(10*4)
print 'len(mem):', len(mem)
print 'mem.address:', MPI.Get_address(mem)
# create a numpy array from the allocated memory
# NOTE: use copy = False here to avoid the copy
buf = np.array(mem, dtype='B', copy=False)
# cast to be int array
npary = np.ndarray(buffer=buf, dtype='i', shape=(10,))
# now you can operate the memory buffer by the usual numpy array operations
npary[:] = np.arange(10)
print 'npary.tobytes:', npary.tobytes()
# release the memory object
MPI.Free_mem(mem)
print 'len(mem) after free:', len(mem)