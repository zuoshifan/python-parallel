# errhandler.py

"""
Demonstrates error handling related operations.

Run this with 1 processes like:
$ mpiexec -n 1 python errhandler.py
or
$ python errhandler.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
win = MPI.Win.Create(MPI.BOTTOM, 1, MPI.INFO_NULL, comm)
fh = MPI.File.Open(comm, 'temp', MPI.MODE_WRONLY | MPI.MODE_CREATE | MPI.MODE_DELETE_ON_CLOSE, MPI.INFO_NULL)

# error handler
for obj, name in [ (comm, 'MPI.Comm'), (win, 'MPI.Win'), (fh, 'MPI.File') ]:
    eh = obj.Get_errhandler()
    default_eh, eh_str = MPI.ERRORS_RETURN, 'MPI.ERRORS_RETURN'
    print 'Default errhandler of %s == %s: %s' % (name, eh_str, eh == default_eh)
    # set error handler to MPI.ERRORS_ARE_FATAL
    obj.Set_errhandler(MPI.ERRORS_ARE_FATAL)
    eh = obj.Get_errhandler()
    assert eh == MPI.ERRORS_ARE_FATAL
    # free the error handler
    eh.Free()
    # eh becomes MPI.ERRHANDLER_NULL after the Free operation
    assert eh ==  MPI.ERRHANDLER_NULL
    # recover the default errhandler
    obj.Set_errhandler(default_eh)
    # call error hander MPI.ERR_OTHER, which is known error not in list
    obj.Call_errhandler(MPI.ERR_OTHER)


fh.Close()

# error class, error code, error string
# add a new error class
errclass = MPI.Add_error_class()
# add an error code to the new error class
errcode = MPI.Add_error_code(errclass)
# associate an error string with an the error errorcode
MPI.Add_error_string(errcode, 'Example error string')
print 'The new error class:', MPI.Get_error_class(errcode)
print 'The new error string:', MPI.Get_error_string(errcode)

# MPI.Exception
# errexc = MPI.Exception(errclass)
# create an MPI.Exception object from MPI.ERR_OTHER
errexc = MPI.Exception(MPI.ERR_OTHER)
print 'MPI.Exception is a subclass of RuntimeError:', isinstance(errexc, RuntimeError)
print 'Error class of MPI.ERR_OTHER:', errexc.Get_error_class()
print 'Error code of MPI.ERR_OTHER:', errexc.Get_error_code()
print 'Error string of MPI.ERR_OTHER:', errexc.Get_error_string()

# show exception catch
try:
    # try to free MPI.COMM_WORLD
    MPI.COMM_WORLD.Free()
except MPI.Exception as e:
    print 'Error class of the Free op:', e.Get_error_class()
    print 'Error code of the Free op:', e.Get_error_code()
    print 'Error string of the Free op:', e.Get_error_string()