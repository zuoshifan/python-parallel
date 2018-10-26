# mpipool_demo3.py

import sys
import numpy as np
from mpipool import MPIPool


# define the function that will be applied to tasks
def worker(task):
    x,y = task
    return 5*x + y**2


class MPIPool1(MPIPool):

    # override method __enter__
    def __enter__(self):
        if not self.is_master():
            self.wait()
            sys.exit(0)

        return super(MPIPool1, self). __enter__()


with MPIPool1() as pool:
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

print 'results:', results