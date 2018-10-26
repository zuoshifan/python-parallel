# mpiutil_funcs.py

"""
Demonstrates the usage of mpilist, mpirange, bcast, gather_list, parallel_map,
split_all, split_local, gather_array, scatter_array.

Run this with 4 processes like:
$ mpiexec -n 4 python mpiutil_funcs.py
"""

import sys
import time
import numpy as np
from caput import mpiutil


rank = mpiutil.rank
size = mpiutil.size

sec = 5 # seconds to wait

def separator(sec, tag):
    # sleep, sync, and flush to avoid output of different parts being mixed
    time.sleep(sec)
    mpiutil.barrier()
    sys.stdout.flush()

    if rank == 0:
        print
        print '-' * 35 + ' ' + tag + ' ' + '-' * 35


# mpilist
separator(sec, 'mpilist')
full_list = [1, 2.5, 'a', True, (3, 4), {'x':1}]
local_list = mpiutil.mpilist(full_list)
print "rank %d has %s with method = 'con'" % (rank, local_list)
local_list = mpiutil.mpilist(full_list, method='alt')
print "rank %d has %s with method = 'alt'" % (rank, local_list)
local_list = mpiutil.mpilist(full_list, method='rand')
print "rank %d has %s with method = 'rand'" % (rank, local_list)

# mpirange
separator(sec, 'mpirange')
local_ary = mpiutil.mpirange(1, 7)
print "rank %d has %s with method = 'con'" % (rank, local_ary)
local_ary = mpiutil.mpirange(1, 7, method='alt')
print "rank %d has %s with method = 'alt'" % (rank, local_ary)
local_ary = mpiutil.mpirange(1, 7, method='rand')
print "rank %d has %s with method = 'rand'" % (rank, local_ary)

# bcast
separator(sec, 'bcast')
if rank == 0:
    sendobj = 'obj'
else:
    sendobj = None
sendobj = mpiutil.bcast(sendobj, root=0)
print 'rank %d has sendobj = %s after bcast' % (rank, sendobj)

# gather_list
separator(sec, 'gather_list')
if rank == 0:
    lst = [0.5, 2]
elif rank == 1:
    lst = ['a', False, 'xy']
elif rank == 2:
    lst = [{'x': 1}]
else:
    lst = []
lst = mpiutil.gather_list(lst, root=None)
print 'rank %d has %s after gather_list' % (rank, lst)

# parallel_map
separator(sec, 'parallel_map')
glist = range(6)
result = mpiutil.parallel_map(lambda x: x*x, glist, root=0)
if rank == 0:
    print 'result = %s' % result

# split_all
separator(sec, 'split_all')
print 'rank %d has: %s' % (rank, mpiutil.split_all(6))

# split_local
separator(sec, 'split_local')
print 'rank %d has: %s' % (rank, mpiutil.split_local(6))

# gather_array
separator(sec, 'gather_array')
if rank == 0:
    local_ary = np.array([[0, 1], [6, 7]])
elif rank == 1:
    local_ary = np.array([[2], [8]])
elif rank == 2:
    local_ary = np.array([[3], [9]])
if rank == 3:
    local_ary = np.array([[4, 5], [10, 11]])
global_ary = mpiutil.gather_array(local_ary, axis=1, root=0)
if rank == 0:
    print 'global_ary = %s' % global_ary

# scatter_array
separator(sec, 'scatter_array')
local_ary = mpiutil.scatter_array(global_ary, axis=1, root=0)
print 'rank %d has local_ary = %s' % (rank, local_ary)
