# file_view.py

"""
Demonstrates the usage of Open, Set_view, Get_view, Close.

Run this with 2 processes like:
$ mpiexec -n 2 python file_view.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

filename = 'temp.txt'
# open the file, create it if it does not exist
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

disp = 5 * 4
etype = MPI.INT

# construct filetype
INT2 = MPI.INT.Create_contiguous(2)
filetype = INT2.Create_contiguous(6)
filetype.Commit()

# set the file view
fh.Set_view(disp, etype, filetype)

print 'file view: ', fh.Get_view()

# close the file
fh.Close()