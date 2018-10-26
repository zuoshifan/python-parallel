# ini.py

"""
Demonstrates the useage of initialization and runtime configuration options.

Run this with 2 processes like:
$ mpiexec -n 2 python ini.py
"""

# mpi4py.rc(initialize=False)
# or use the following way

# we must set the initialization and runtime configuration options
# before the import of MPI module
from mpi4py import rc
# the default of rc.initialize is True and rc.finalize is None
# change rc.initialize to False
# rc.finalize will also be False when it value is None
rc.initialize = False

from mpi4py import MPI
print 'Before call Init(), MPI.Is_initialized: %s' % MPI.Is_initialized()
print 'Before call Init(), MPI.Is_finalized: %s' % MPI.Is_finalized()

# now we have to call Init explicitly
MPI.Init()
print 'After call Init(), MPI.Is_initialized: %s' % MPI.Is_initialized()
print 'After call Init(), MPI.Is_finalized: %s' % MPI.Is_finalized()

comm = MPI.COMM_WORLD
rank = comm.rank

print 'I am Process %d...' % rank

# have to call Finalize explicitly to terminate MPI
MPI.Finalize()
print 'After call Finalize(), MPI.Is_initialized: %s' % MPI.Is_initialized()
print 'After call Finalize(), MPI.Is_finalized: %s' % MPI.Is_finalized()