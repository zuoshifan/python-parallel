# greq.py

"""
Demonstrates the usage of generalized request.

Run this with 1 processes like:
$ mpiexec -n 1 python greq.py
or
$ python greq.py
"""

import time
import threading
from mpi4py import MPI


comm = MPI.COMM_WORLD

def query_fn(status, *args, **kargs):
    print 'Call query_fn with args = %s, kargs = %s...' % (args, kargs)
    status.source = MPI.UNDEFINED
    status.tag = MPI.UNDEFINED
    status.cancelled = False
    status.Set_elements(MPI.BYTE, 0)

    return MPI.SUCCESS

def free_fn(*args, **kargs):
    print 'Call free_fn with args = %s, kargs = %s...' % (args, kargs)
    if 'a' in kargs:
        # change the kargs argument (have effect only for changeable type like list, dict, etc)
        print "Append 3 to kargs['a']"
        kargs['a'].append(3)

    return MPI.SUCCESS

def cancel_fn(completed, *args, **kargs):
    print 'Call cancel_fn with completed = %s, args = %s, kargs = %s...' % (completed, args, kargs)

    return MPI.SUCCESS

# define an user-defined non-blocking operate
def iop(*args, **kargs):

    def compute(greq):
        # sleep 1 second to simulate a compute-intensive task
        time.sleep(1.0)

        # call Complete method to inform MPI implementation that
        # the operation associated with this greq has completed
        greq.Complete()

    # create a generalized request
    greq = MPI.Grequest.Start(query_fn, free_fn, cancel_fn, args=args, kargs=kargs)
    # call compute in a separate thread, so it will not block the return of this
    iop_thread = threading.Thread(target=compute, name='iop_thread', args=(greq,))
    iop_thread.daemon = True
    # start the thread
    iop_thread.start()

    return greq


a = []
print 'Before the cal of iop, a = %s' % a

# call the user-defined non-blocking operation,
# which will return a MPI.Grequest object immediately
greq = iop(1, 2, a=a)

# test if the non-blocking operate is completed
status = MPI.Status()
print 'Is complete: %s' % greq.Test(status)
print 'source = %d, tag = %d, cancelled = %s, count = %d' % (status.source, status.tag, status.cancelled, status.count)

# call Cancel
greq.Cancel()
print 'Is complete: %s' % greq.Test()

# wait 1 second for the complete of iop
time.sleep(1.0)

# call Cancel
greq.Cancel()
print 'Is complete: %s' % greq.Test(status)
print 'source = %d, tag = %d, cancelled = %s, count = %d' % (status.source, status.tag, status.cancelled, status.count)

try:
    # call Cancel after the complete of iop, wich will throw an exception
    greq.Cancel()
except MPI.Exception as e:
    print e.error_string

print 'After the complete of iop, a = %s' % a