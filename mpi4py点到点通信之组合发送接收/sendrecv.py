# sendrecv.py

from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

tag = 123
left = rank - 1 if rank >=1 else size - 1
right = rank + 1 if rank < size - 1 else 0

send_obj = {'obj': rank}

recv_obj = comm.sendrecv(send_obj, dest=right, sendtag=tag, source=left, recvtag=tag)
print 'process %d sends %s' % (rank, send_obj)
print 'process %d receives %s' % (rank, recv_obj)
