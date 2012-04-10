import socket
import sys

# Create a TCP/IP socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10002)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
temp_list = []

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
