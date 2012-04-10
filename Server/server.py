import socket
import sys

class server:
  def __init__(self, port_id):
    # Create a TCP/IP socket

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port

    self.server_address = ('localhost', 10000)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    self.sock.bind(server_address)

    # Listen for incoming connections
    self.sock.listen(1)
    self.temp_list = []

  def run_server():
    while True:
    # wait for connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
      print >>sys.stderr, 'connection from', client_address

      # Recieve the data in small chunks and retransmit it
      while True:
        data = connection.recv(16)
        temp_list.append(data)
        print >>sys.stderr, 'received "%s"' % data
        if data:
          print >>sys.stderr, 'sending data back to the client'
          connection.sendall(data)
        else:
          print >>sys.stderr, 'no more data from', client_address
          break

      print "Temp List: ", temp_list
      list_r = eval(temp_list[0])
      print "The final list is: ", list_r

    finally:
       # Clean up the connection
       connection.close()
