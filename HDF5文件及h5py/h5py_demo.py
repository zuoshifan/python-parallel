# h5py_demo.py

"""
Demonstrates how to use h5py.

Run this like:
$ python h5py_demo.py
"""

import os
import numpy as np
import h5py

file_name = 'test.hdf5'
# create a new HDF5 file
f = h5py.File(file_name)
# create a new group
f.create_group('/grp1') # or f.create_group('grp1')
# create a nother group inside grp1
f.create_group('/grp1/grp2') # or f.create_group('grp1/grp2')
# create a dataset in group "/"
data = np.arange(6).reshape(2, 3)
f.create_dataset('dset1', data=data) # or f.create_dataset('/dset1', data=data)
# create another dataset in group /grp1
f.create_dataset('grp1/dset2', data=data) # or f.create_dataset('/grp1/dset2', data=data)
# create an attribute of "/"
f.attrs['a'] = 1 # or f.attrs['/a'] = 1
# create an attribute of group "/grp1"
f['grp1'].attrs['b'] = 'xyz'
# create an attribute of dataset "/grp1/dset2"
f['grp1/dset2'].attrs['c'] = np.array([1, 2])
# close file
f.close()

# open the existing test.hdf5 for read only
f = h5py.File(file_name, 'r')
# read dataset /dset1
print '/dset1 = %s' % f['dset1'][:]
# read dataset /grp1/dset2
print '/grp1/dset2 = %s' % f['/grp1/dset2'][:]
# get attributes
print f.attrs['a']
print f['grp1'].attrs['b']
print f['grp1/dset2'].attrs['c']

# remove the created file
os.remove(file_name)