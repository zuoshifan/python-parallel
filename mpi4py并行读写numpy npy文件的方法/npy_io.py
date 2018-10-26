# npy_io.py

"""
Demonstrates how to use mpi4py to write/read numpy array to/from npy file.

Run this with 2 processes like:
$ mpiexec -n 2 python npy_io.py
"""

import warnings
import numpy as np
import format as fm
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def typemap(dtype):
    """Map a numpy dtype into an MPI_Datatype.

    Parameters
    ----------
    dtype : np.dtype
        The numpy datatype.

    Returns
    -------
    mpitype : MPI.Datatype
        The MPI.Datatype.

    """
    # Need to try both as the name of the typedoct changed in mpi4py 2.0
    try:
        return MPI.__TypeDict__[np.dtype(dtype).char]
    except AttributeError:
        return MPI._typedict[np.dtype(dtype).char]


def parallel_write_array(filename, local_array, axis=0, version=None, comm=None):
    """
    Parallelly write an array distributed in all processes to an NPY file, including a header.

    Parameters
    ----------
    filename : str
        Name of the file to write array into.
    local_array : ndarray
        The subarray local to this process that will be writen to disk.
    axis : int
        The axis that the array is distributed on.
    version : (int, int) or None, optional
        The version number of the format. None means use the oldest
        supported version that is able to store the data.  Default: None
    comm : mpi4py communicator or None.
        A valid mpi4py communicator or None if no MPI.

    """

    # if no MPI, or only 1 MPI process, call np.save directly
    if comm is None or comm.size == 1:
        np.save(filename, local_array)
        return

    if local_array.dtype.hasobject:
        # contain Python objects
        raise RuntimeError('Currently not support array that contains Python objects')
    if local_array.flags.f_contiguous and not local_array.flags.c_contiguous:
        raise RuntimeError('Currently not support Fortran ordered array')

    local_shape = local_array.shape # shape of local_array
    local_axis_len = local_shape[axis]
    local_axis_lens = comm.allgather(local_axis_len)
    global_axis_len = sum(local_axis_lens)
    global_shape = list(local_shape)
    global_shape[axis] = global_axis_len
    global_shape = tuple(global_shape) # shape of global array
    local_start = [0] * len(global_shape)
    local_start[axis] = np.cumsum([0] + local_axis_lens)[comm.rank] # start of local_array in global array

    # open the file in write only mode
    fh = MPI.File.Open(comm, filename, amode=MPI.MODE_CREATE | MPI.MODE_WRONLY)

    # check validity of version
    fm._check_version(version)
    # first write the array header to file by process 0
    if comm.rank == 0:
        # get the header, which is a dict
        header = fm.header_data_from_array_1_0(local_array)
        # update the shape value to shape of the global array
        header['shape'] = global_shape
        # write header to file
        used_ver = fm._write_array_header(fh, header, version)
        # this warning can be removed when 1.9 has aged enough
        if version != (2, 0) and used_ver == (2, 0):
            warnings.warn("Stored array in format 2.0. It can only be"
                        "read by NumPy >= 1.9", UserWarning, stacklevel=2)

        # get the position of the individual file pointer,
        # which is now at the end of the file
        pos = fh.Get_position()
    else:
        pos = 0

    # broadcast the end position of the file to all processes
    pos = comm.bcast(pos, root=0)

    # get the etype
    etype = typemap(local_array.dtype)

    # construct the filetype
    filetype = etype.Create_subarray(global_shape, local_shape, local_start, order=MPI.ORDER_C)
    filetype.Commit()

    # set the file view
    fh.Set_view(pos, etype, filetype, datarep='native')

    # collectively write the array to file
    fh.Write_all(local_array)

    # close the file
    fh.Close()


def parallel_read_array(filename, axis=0, comm=None):
    """
    Parallelly read an array from an NPY file, each process reads its own part.

    Parameters
    ----------
    filename : str
        Name of the file constains the array.
    axis : int
        The axis to distribute the array on each process.
    comm : mpi4py communicator or None.
        A valid mpi4py communicator or None if no MPI.

    Returns
    -------
    local_array : ndarray
        The array local to this process from the data on disk.

    """

    # if no MPI, or only 1 MPI process, call np.load directly
    if comm is None or comm.size == 1:
        return np.load(filename)

    # open the file in read only mode
    fh = MPI.File.Open(comm, filename, amode=MPI.MODE_RDONLY)

    # read and check version of the npy file
    version = fm.read_magic(fh)
    fm._check_version(version)
    # get shape, order, dtype info of the array
    global_shape, fortran_order, dtype = fm._read_array_header(fh, version)

    if dtype.hasobject:
        # contain Python objects
        raise RuntimeError('Currently not support array that contains Python objects')
    if fortran_order:
        raise RuntimeError('Currently not support Fortran ordered array')

    local_shape = list(global_shape)
    axis_len = local_shape[axis]
    base = axis_len / comm.size
    rem = axis_len % comm.size
    part = base * np.ones(comm.size, dtype=np.int) + (np.arange(comm.size) < rem).astype(np.int)
    bound = np.cumsum(np.insert(part, 0, 0))
    local_shape[axis] = part[comm.rank] # shape of local array
    local_start = [0] * len(global_shape)
    local_start[axis] = bound[comm.rank] # start of local_array in global array

    # allocate space for local_array to hold data read from file
    local_array = np.empty(local_shape, dtype=dtype, order='C')

    # get the position of the individual file pointer,
    # which is at the end of the header, the start of array data
    pos = fh.Get_position()

    # get the etype
    etype = typemap(dtype)

    # construct the filetype
    filetype = etype.Create_subarray(global_shape, local_shape, local_start, order=MPI.ORDER_C)
    filetype.Commit()

    # set the file view
    fh.Set_view(pos, etype, filetype, datarep='native')

    # collectively read the array from file
    fh.Read_all(local_array)

    # close the file
    fh.Close()

    return local_array


filename = 'test.npy'
local_array = np.arange(12, dtype='i').reshape(3, 4)

# parallelly write local array to file, assume array is distributed on axis 1, i.e., column
parallel_write_array(filename, local_array, axis=1, comm=comm)

# check data in the file
if rank == 0:
    print 'data in file: %s' % np.load(filename)

# now parallelly read data from file, each process read several row of the array
print 'process %d read: %s' % (rank, parallel_read_array(filename, axis=0, comm=comm))
