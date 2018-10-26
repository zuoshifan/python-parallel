# attrs.py


"""
Demonstrates the usage of attribute and name operations.

Run this with 1 processes like:
$ mpiexec -n 1 python attrs.py
or
$ python attrs.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
win = MPI.Win.Create(MPI.BOTTOM, 1, MPI.INFO_NULL, comm)
dtype = MPI.INT

def copy_fn(o, k, v):
    print 'inside copy_fn: o = %s, k = %s, v = %s' % (o, k, v)
    return v

def del_fn(o, k, v):
    print 'inside delete_fn: o = %s, k = %s, v = %s' % (o, k, v)

for cls, cls_name, obj, obj_name in [ (MPI.Comm, 'MPI.Comm', comm, 'MPI.COMM_WORLD'),
                                      (MPI.Datatype, 'MPI.Datatype', dtype, 'MPI.INT'),
                                      (MPI.Win, 'MPI.Win', win, 'win') ]:
    # use the default copy_fn and delete_fn
    keyval = cls.Create_keyval()
    attr = obj.Get_attr(keyval)
    print 'before Set_attr of %s: attr = %s' % (obj_name, attr)
    # can set attr as a Python list only if nopython is False (the default)
    obj.Set_attr(keyval, [1, 2, 3])
    attr = obj.Get_attr(keyval)
    print 'after Set_attr of %s: attr = %s' % (obj_name, attr)
    obj.Delete_attr(keyval)
    attr = obj.Get_attr(keyval)
    print 'after Delete_attr of %s: attr = %s' % (obj_name, attr)
    keyval = cls.Free_keyval(keyval)
    print 'after Free_keyval of %s keyval == MPI.KEYVAL_INVALID: %s' % (obj_name, keyval == MPI.KEYVAL_INVALID)

    # use customed copy_fn and delete_fn, and set nopython = True
    keyval = cls.Create_keyval(copy_fn=copy_fn, delete_fn=del_fn, nopython=True)
    attr = obj.Get_attr(keyval)
    print 'before Set_attr of %s: attr = %s' % (obj_name, attr)
    obj.Set_attr(keyval, 123)
    attr = obj.Get_attr(keyval)
    print 'after Set_attr of %s: attr = %s' % (obj_name, attr)
    if hasattr(obj, 'Dup'):
        dup = obj.Dup()
        attr = dup.Get_attr(keyval)
        print 'after Dup of %s: attr = %s' % (obj_name, attr)
    obj.Delete_attr(keyval)
    attr = obj.Get_attr(keyval)
    print 'after Delete_attr of %s: attr = %s' % (obj_name, attr)
    keyval = cls.Free_keyval(keyval)
    print 'after Free_keyval of %s keyval == MPI.KEYVAL_INVALID: %s' % (obj_name, keyval == MPI.KEYVAL_INVALID)

    # name operations
    print 'default name of %s: %s' % (obj_name, obj.Get_name())
    if cls_name == 'MPI.Comm':
        print 'default name of MPI.COMM_SELF: %s' % MPI.COMM_SELF.Get_name()
    obj.Set_name('new_name')
    print 'name of %s after Set_name: %s' % (obj_name, obj.Get_name())