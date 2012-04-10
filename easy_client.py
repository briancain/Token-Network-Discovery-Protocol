import socket
import sys

###############################################################

#   CIS 598 Senior Project by Brian Cain

#   bccain@ksu.edu

#   easy_client.py - A client for the node class

###############################################################

class client:
  def __init__(self, port_id, flag):
    """Create a dictionary mapping socket module constants to their names."""
    self.families = dict((getattr(socket, n), n)
                   for n in dir(socket)
                   if n.startswith('AF_'))
    self.types = dict((getattr(socket, n), n)
                   for n in dir(socket)
                   if n.startswith('SOCK_'))
    self.protocols = dict((getattr(socket, n), n)
                   for n in dir(socket)
                   if n.startswith('IPPROTO_'))

    # Create a TCP/IP socket
    self.port = 10000 + port_id
    self.sock = socket.create_connection(('localhost', self.port))

    if flag:
      print >>sys.stderr, 'Family  :', self.families[self.sock.family]
      print >>sys.stderr, 'Type    :', self.types[self.sock.type]
      print >>sys.stderr, 'Protocol:', self.protocols[self.sock.proto]
      print >>sys.stderr

  def run_client(self):
    try:
     
      # Send data
      # message = raw_input("Enter your message to send to the server: ")
      data_message = (11, 22, 33) # example disco_msg
      message = repr(data_message)
      print >>sys.stderr, 'sending "%s"' % message
      sock.sendall(message)

      amount_received = 0
      amount_expected = len(message)
      
      while amount_received < amount_expected:
          data = sock.recv(16)
          amount_received += len(data)
          print >>sys.stderr, 'received "%s"' % data

    finally:
      print >>sys.stderr, 'closing socket'
      sock.close()

  
