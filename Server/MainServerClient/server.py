try:
  import cPickle as pickle
except:
  import pickle

import socket
import sys

###############################################################

#   CIS 598 Senior Project by Brian Cain

#   bccain@ksu.edu

#   server.py - Server Class for node

###############################################################

class server:
  def __init__(self, port_id, flag):
    # Create a TCP/IP socket

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port

    self.port = 10000 + port_id

    self.server_address = ('localhost', self.port)
    print >>sys.stderr, 'starting up on %s port %s' % self.server_address
    self.sock.bind(self.server_address)

    # Listen for incoming connections
    self.sock.listen(1)
    self.temp_list = []

  def run_server(self):
    while True:
      # wait for connection
      print >>sys.stderr, 'waiting for a connection'
      connection, client_address = self.sock.accept()

      try:
        print >>sys.stderr, 'connection from', client_address

        # Recieve the data in small chunks and retransmit it
        while True:
          data = connection.recv(16)
          self.temp_list.append(data)
          print >>sys.stderr, 'received "%s"' % data
          if data:
            self.temp_list.append(data)
            print >>sys.stderr, 'sending data back to the client'
            connection.sendall(data)
          else:
            print >>sys.stderr, 'no more data from', client_address
            break

        join_ans = "".join(self.temp_list)
        ans = pickle.load(join_ans)
      
      finally:
         # Clean up the connection
         connection.close()

      return ans

