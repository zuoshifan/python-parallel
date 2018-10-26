# info.py

"""
Demonstrates the usage of info and assertion.

Run this with 1 processes like:
$ mpiexec -n 1 python info.py
or
$ python info.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD

# create an info object
info = MPI.Info.Create()
# dupicate the info
info1 = info.Dup()
# free the duplicated info
info1.Free()
# becomes MPI.INFO_NULL after the free op
assert info1 == MPI.INFO_NULL

try:
    # try to delete a non-existed key from info
    info.Delete('a')
except MPI.Exception as e:
    print e.error_string

# set key and value
info.Set('k1', 'v1')
info.Set('k2', 'v2')
info.Set('k3', 'v3')
print 'k1:', info.Get('k1')
print 'nkeys:', info.Get_nkeys()
print 'the second key:', info.Get_nthkey(1)

try:
    # try to set a key with length > MPI.MAX_INFO_KEY
    info.Set('k' * (MPI.MAX_INFO_KEY + 1), 'v')
except MPI.Exception as e:
    print e.error_string

try:
    # try to set a value with length > MPI.MAX_INFO_VAL
    info.Set('k', 'v' * (MPI.MAX_INFO_VAL + 1))
except MPI.Exception as e:
    print e.error_string

# dict interface
print 'len(info):', len(info)
print 'k1 in info:', 'k1' in info
# __iter__ method
for k in info:
    print k
info['k4'] = 'v4'
print 'k4:', info['k4']
del info['k4']
print 'k4:', info.get('k4', 'v4_new')
print 'keys:', info.keys()
print 'values:', info.values()
print 'items:', info.items()
info.update({'k1': 'v1_new', 'k5': 'k5_new'})
print 'items after update:', info.items()
info.clear()
print 'items after clea:', info.items()

# info with comm
comm_info = MPI.Info.Create()
comm.Set_info(comm_info)
comm.Get_info()
info_dup = MPI.Info.Create()
comm.Dup_with_info(info_dup)

# comm_info = MPI.Info.Create()
# comm_info['mpi_assert_no_any_tag'] = 'true'
# print comm_info.items()
# comm.Set_info(comm_info)
# print comm.Get_info().items()
# # comm_dup = comm.Dup_with_info(MPI.Info.Create())
# info_dup = MPI.Info.Create()
# info_dup['mpi_assert_no_any_source'] = 'true'
# comm_dup = comm.Dup_with_info(info_dup)
# print comm_dup.info.items()