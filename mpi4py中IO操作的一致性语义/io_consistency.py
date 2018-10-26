# io_consistency.py

"""
Demonstrates how to achive consistency semantics.

Run this with 2 processes like:
$ mpiexec -n 2 python io_consistency.py
"""


import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

buf1 = bytearray(range(100*rank, 100*(rank+1)))
buf2 = bytearray([0]*100)

filename = 'temp.txt'

# access non-overlapping areas in file
# ------------------------------------------------------------------------------

# open the file, create it if it does not exist and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

if rank == 0:
    fh.Write_at(0, [buf1, 100, MPI.BYTE])
    fh.Read_at(0, [buf2, 100, MPI.BYTE])
    print buf2 == buf1
elif rank == 1:
    fh.Write_at(100, [buf1, 100, MPI.BYTE])
    fh.Read_at(100, [buf2, 100, MPI.BYTE])
    print buf2 == buf2

# close the file
fh.Close()


# reinitialize buf2
buf2 = bytearray([0]*100)

# set atomicity
# ------------------------------------------------------------------------------

# open the file, create it if it does not exist and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

# set atomicity
fh.Set_atomicity(True)

if rank == 0:
    fh.Write_at(0, [buf1, 100, MPI.BYTE])
elif rank == 1:
    fh.Write_at(100, [buf1, 100, MPI.BYTE])

# use Barrier synchronizition to make sure read after the completion of write
comm.Barrier()

if rank == 0:
    fh.Read_at(100, [buf2, 100, MPI.BYTE])
    print buf2 == bytearray(range(100, 200))
elif rank == 1:
    fh.Read_at(0, [buf2, 100, MPI.BYTE])
    print buf2 == bytearray(range(0, 100))

# close the file
fh.Close()


# reinitialize buf2
buf2 = bytearray([0]*100)

# close the file and reopen it
# ------------------------------------------------------------------------------

# open the file for write only, create it if it does not exist
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_WRONLY)

if rank == 0:
    fh.Write_at(0, [buf1, 100, MPI.BYTE])
elif rank == 1:
    fh.Write_at(100, [buf1, 100, MPI.BYTE])

# close the file
fh.Close()

# use Barrier synchronizition to make reopen is after the completion of the close
comm.Barrier()

# reopen the file
fh = MPI.File.Open(comm, filename, amode=MPI.MODE_RDONLY | MPI.MODE_DELETE_ON_CLOSE)

if rank == 0:
    fh.Read_at(100, [buf2, 100, MPI.BYTE])
    print buf2 == bytearray(range(100, 200))
elif rank == 1:
    fh.Read_at(0, [buf2, 100, MPI.BYTE])
    print buf2 == bytearray(range(0, 100))

# close the file
fh.Close()


# reinitialize buf2
buf2 = bytearray([0]*100)

# use Sync to separate diffrent sequences
# ------------------------------------------------------------------------------

# open the file, create it if it does not exist and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

# process 0 starts a write sequence first
if rank == 0:
    fh.Write_at(0, [buf1, 100, MPI.BYTE])

fh.Sync()

# use a Barrier synchronizition to separate process 0's write sequence from
# process 1's write sequence in time
comm.Barrier()

# process 1 starts its write sequence then
fh.Sync()

if rank == 1:
    fh.Write_at(100, [buf1, 100, MPI.BYTE])

fh.Sync()

# use a Barrier synchronizition to separate process 1's write sequence from
# the next sequence in time                                |
comm.Barrier()

fh.Sync()

# process 1 and 2 start their read sequence
if rank == 0:
    fh.Read_at(100, [buf2, 100, MPI.BYTE])
    print buf2 == bytearray(range(100, 200))
elif rank == 1:
    fh.Read_at(0, [buf2, 100, MPI.BYTE])
    print buf2 == bytearray(range(0, 100))

# close the file
fh.Close()


# reinitialize buf2
buf2 = bytearray([0]*100)

# set atomicity and collective write
# ------------------------------------------------------------------------------

# open the file, create it if it does not exist and delete it on close
fh = MPI.File.Open(comm, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE)

# set atomicity
fh.Set_atomicity(True)

# use collective write
if rank == 0:
    fh.Write_at_all(0, [buf1, 100, MPI.BYTE])
elif rank == 1:
    fh.Write_at_all(100, [buf1, 100, MPI.BYTE])

# no need Barrier here
# comm.Barrier()

if rank == 0:
    fh.Read_at(100, [buf2, 100, MPI.BYTE])
    print buf2 == bytearray(range(100, 200))
elif rank == 1:
    fh.Read_at(0, [buf2, 100, MPI.BYTE])
    print buf2 == bytearray(range(0, 100))

# close the file
fh.Close()


# reinitialize buf2
buf2 = bytearray([0]*100)

# use MPI.COMM_SELF to open the file
# ------------------------------------------------------------------------------

# open the file, create it if it does not exist and delete it on close
fh = MPI.File.Open(MPI.COMM_SELF, filename, amode= MPI.MODE_CREATE | MPI.MODE_RDWR | MPI.MODE_DELETE_ON_CLOSE) # NOTE here we use MPI.COMM_SELF

# process 0 starts a write sequence first
if rank == 0:
    fh.Write_at(0, [buf1, 100, MPI.BYTE])

    fh.Sync()

# use a Barrier synchronizition to separate process 0's write sequence from
# process 1's write sequence in time
comm.Barrier()

# process 1 starts its write sequence then
if rank == 1:
    fh.Sync()
    fh.Write_at(100, [buf1, 100, MPI.BYTE])
    fh.Sync()

# use a Barrier synchronizition to separate process 1's write sequence from
# the next sequence in time                                |
comm.Barrier()

# process 1 and 2 start their read sequence
if rank == 0:
    fh.Sync()
    fh.Read_at(100, [buf2, 100, MPI.BYTE])
    print buf2 == bytearray(range(100, 200))
elif rank == 1:
    fh.Read_at(0, [buf2, 100, MPI.BYTE])
    print buf2 == bytearray(range(0, 100))

# close the file
fh.Close()