# inter_comm_bcast.py

from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 1:
    obj = {'a': 1}
else:
    obj = None

# split comm into three new communicators according to `color`
color = rank % 3
comm_split = comm.Split(color=color, key=rank)
# group 0 with color = 0 -> rank = {0, 3, 6}
# group 1 with color = 1 -> rank = {1, 4, 7}
# group 2 with color = 2 -> rank = {2, 5, 8}

# broadcast `obj` from rank 0 of group1 (rank 1 of COMM_WORLD) to all process in group 2
if color == 1:
    # create an inter-communicator by using rank 0 of local_comm and rank 2 of MPI.COMM_WORLD
    comm_inter = comm_split.Create_intercomm(0, comm, 2, tag=12)
    if comm_inter.rank == 0:
        root = MPI.ROOT
    else:
        root = MPI.PROC_NULL
    comm_inter.bcast(obj, root=root)
elif color == 2:
    # create an inter-communicator by using rank 0 of local_comm and rank 1 of MPI.COMM_WORLD
    comm_inter = comm_split.Create_intercomm(0, comm, 1, tag=12)
    obj = comm_inter.bcast(obj, root=0)

print 'rank %d has %s' % (rank, obj)
