# mpipool_demo.py

import sys
import numpy as np
from mpipool import MPIPool


# define the function that will be applied to tasks
def worker(task):
    x, y = task
    return x**2 + 2*y


# create the pool
pool = MPIPool()

# only run map() on the master process, all other processes wait for their work
if not pool.is_master():
    pool.wait()
    # worker processes exit after they have done their work
    sys.exit(0)

# the following code is executed by the master process only
# create some random input data
x = np.random.uniform(size=10)
y = np.random.uniform(size=10)
tasks = list(zip(x, y))

# crate a callback function
def cb(x):
    print x

# map the function worker to tasks
# and execute them parallel by processes other than the master
results = pool.map(worker, tasks, callback=cb)

# close the pool
pool.close()

print 'results:', results