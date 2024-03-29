try:
  import cPickle as pickle
except:
  import pickle

import pprint
from StringIO import StringIO

import socket
import sys

# Create a TCP/IP socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

list_ans = []

while True:
  # wait for connection
  print >>sys.stderr, 'waiting for a connection'
  connection, client_address = sock.accept()

  try:
    print >>sys.stderr, 'connection from', client_address

    # Recieve the data in small chunks and retransmit it
    while True:
      data = connection.recv(16)
      print >>sys.stderr, 'received "%s"' % data
      if data:
        list_ans.append(data)
        print >>sys.stderr, 'sending data back to the client'
        connection.sendall(data)
      else:
        print >>sys.stderr, 'no more data from', client_address
        break
    
    # needed to reconstruct pickle string
    print "List_ans = ", list_ans
    join_ans = "".join(list_ans)
    ans = pickle.loads(join_ans)
    print "answer = ", ans

  finally:
     # Clean up the connection
     connection.close()
