# spawn_multiple_master.py

"""
Demonstrates the usage of Spawn_multiple, Disconnect.

Run this with 1 process like:
$ mpiexec -n 1 python spawn_multiple_master.py
# or
$ python spawn_multiple_master.py
"""

import sys
import numpy as np
from mpi4py import MPI

# create one new process to execute spawn_slave1.py, and two new processes to execute spawn_slave2.py
commands = [sys.executable] * 2
args    = [['spawn_slave1.py'], ['spawn_slave2.py']]
maxprocs = [1, 2]
comm = MPI.COMM_WORLD.Spawn_multiple(commands, args, maxprocs)

# disconnect and free comm
comm.Disconnect()