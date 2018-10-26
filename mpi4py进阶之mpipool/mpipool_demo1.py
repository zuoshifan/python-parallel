# mpipool_demo1.py

import numpy as np
from mpipool import MPIPool


# define the function that will be applied to tasks
def worker(task):
    x,y = task
    return 5*x + y**2


with MPIPool() as pool:
    # only run map() on the master process, all other processes wait for their work
    if not pool.is_master():
        pool.wait()
    else:
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

print 'Done!'