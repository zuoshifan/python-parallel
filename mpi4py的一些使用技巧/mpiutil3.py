# mpiutil3.py

"""Utilities for making MPI usage transparent."""

import sys
import warnings
from types import ModuleType


rank = 0
size = 1
comm = None

## try to setup MPI and get the comm, rank and size
## if not they should end up as comm = None, rank=0, size=1
try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD

    rank = comm.Get_rank()
    size = comm.Get_size()

except ImportError:
    warnings.warn("Warning: mpi4py not installed.")


def reduce(sendobj, root=0, op=None, comm=comm):
    if comm is not None and comm.size > 1:
        return comm.reduce(sendobj, root=root, op=(op or MPI.SUM))
    else:
        return sendobj


# this is a thin wrapper around THIS module (we patch sys.modules[__name__])
class SelfWrapper(ModuleType):
    def __init__(self, self_module, baked_args={}):
        for attr in ["__file__", "__hash__", "__buildins__", "__doc__", "__name__", "__package__"]:
            setattr(self, attr, getattr(self_module, attr, None))

        self.self_module = self_module

    def __getattr__(self, name):
        if name in globals():
            return globals()[name]
        elif comm is not None and name in MPI.__dict__:
            return MPI.__dict__[name]

    def __call__(self, **kwargs):
        # print 'here'
        return SelfWrapper(self.self_module, kwargs)


self = sys.modules[__name__]
sys.modules[__name__] = SelfWrapper(self)