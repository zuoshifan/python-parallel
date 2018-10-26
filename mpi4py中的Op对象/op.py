# op.py

"""
Demonstrates the usage of MPI.Op.

Run this with 2 processes like:
$ mpiexec -n 2 python op.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.rank

def mysum_obj(a, b):
    # sum of pythn objects
    return a + b

def mysum_buf(a, b, dt):
    assert dt == MPI.INT
    assert len(a) == len(b)

    def to_nyarray(a):
        # convert a MPI.memory object to a numpy array
        size = len(a)
        buf = np.array(a, dtype='B', copy=False)
        return np.ndarray(buffer=buf, dtype='i', shape=(size / 4,))

    to_nyarray(b)[:] = mysum_obj(to_nyarray(a), to_nyarray(b))

def mysum(ba, bb, dt):
    if dt is None:
        # ba, bb are python objects
        return mysum_obj(ba, bb)
    else:
        # ba, bb are MPI.memory objects
        return mysum_buf(ba, bb, dt)

commute = True
# create a user-defined operator by using function mysum
myop = MPI.Op.Create(mysum, commute)
print 'myop.is_commutative: %s' % myop.is_commutative
print 'myop.is_predefined: %s' % myop.is_predefined

# call the op on different objects
print 'myop(1, 2) = %s' % myop(1, 2)
print 'myop([1], [2]) = %s' % myop([1], [2])
print 'myop(np.array([1]), np.array([2])) = %s' % myop(np.array([1]), np.array([2]))

a = np.arange(3, dtype='i')
b = np.zeros(3, dtype='i')
# use the user-defined myop in allreduce
comm.Allreduce(a, b, op=myop)
# or
# comm.Allreduce([a, MPI.INT], [b, MPI.INT], op=myop)
print 'Allreduce: b = %s' % b

print 'allreduce 2: %s' % comm.allreduce(2, op=myop)
print 'allreduce [2]: %s' % comm.allreduce([2], op=myop)

inbuf = np.arange(4*rank, 4*(rank+1), dtype ='i')
inoutbuf = np.array([10, 10, 10, 10], dtype='i')
myop.Reduce_local(inbuf, inoutbuf)
print 'Reduce_local with myop: %s' % inoutbuf

# free the user-defined op
myop.Free()

# use the predefined op
print 'isinstance(MPI.MAX, MPI.Op): %s' % isinstance(MPI.MAX, MPI.Op)
print 'MPI.MAX.is_predefined: %s' % MPI.MAX.is_predefined

inbuf = np.array([1, 2], dtype='i')
inoutbuf = np.array([2, 0], dtype='i')
MPI.MAX.Reduce_local(inbuf, inoutbuf)
print 'Reduce_local with MPI.MAX: %s' % inoutbuf

try:
    # try to free the predefined op
    MPI.MAX.Free()
except MPI.Exception as e:
    print e.error_string