# server.py

"""
Server side of the MPI client/server programming model.

Run this with 1 processes like:
$ mpiexec -n 1 python server.py
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD

service_name = 'compute'
# open a port
port_name = MPI.Open_port()
# bind the opened port to a service_name,
# client can connect to the port by looking-up this service_name
MPI.Publish_name(service_name, port_name)
# wait for client to connect
inter_comm = comm.Accept(port_name)

# receive message from client
recv_obj = inter_comm.recv(source=0, tag=0)
print 'Server receives %s from client.' % recv_obj
send_obj = eval(recv_obj)
# reply the result to the client
print 'Server sends %s to client.' % send_obj
inter_comm.send(send_obj, dest=0, tag=1)

# unpublish the service_name, close the port and disconnect
MPI.Unpublish_name(service_name, port_name)
MPI.Close_port(port_name)
inter_comm.Disconnect()
