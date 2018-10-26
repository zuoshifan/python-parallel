# inter_comm.py

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print 'Is MPI.COMM_WORLD a inter-communicator:', comm.Is_inter()

# split comm into two new communicators according to `color`
color = rank % 2
comm_split = comm.Split(color=color, key=rank)

if color == 0:
    # create an inter-communicator by using rank 0 of local_comm and rank 1 of MPI.COMM_WORLD
    comm_inter = comm_split.Create_intercomm(0, comm, 1, tag=12)
    if comm_inter.rank == 0:
        # rank 0 of local_comm sends a message to rank 1 of the remote_comm
        send_obj = {'a': 1}
        comm_inter.send(send_obj, dest=1, tag=1)
        print 'rank %d of comm_inter with color 0 sends %s...' % (comm_inter.rank, send_obj)
elif color == 1:
    # create an inter-communicator by using rank 0 of local_comm and rank 0 of MPI.COMM_WORLD
    comm_inter = comm_split.Create_intercomm(0, comm, 0, tag=12)
    if comm_inter.rank == 1:
        # rank 1 of local_comm receives a message from rank 0 of the remote_comm
        recv_obj = comm_inter.recv(source=0, tag=1)
        print 'rank %d of comm_inter with color 1 receives %s...' % (comm_inter.rank, recv_obj)

print 'Is comm_inter a inter_communicator:', comm_inter.Is_inter()

# merge the two inter-communicators
if color == 0:
    high = True
elif color == 1:
    high = False
comm_merge = comm_inter.Merge(high=high)
print 'rank %d in MPI.COMM_WORLD -> rank %d in comm_merge' % (rank, comm_merge.rank)