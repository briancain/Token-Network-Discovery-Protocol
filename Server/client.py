import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
  # Send data
  message = 'This is the message. It will be repeated.'
  print >>sys.stderr, 'sending %s' % message
  sock.sendall(message)

  # Look for the response
  amount_recieved = 0
  amount_expected = len(message)

  while amount_recieved < amount_expected:
    data = sock.recv(16)
    amount_recieved += len(data)
    print >>sys.stderr, 'recieved "%s"' % data

finally:
  print >>sys.stderr, 'closing socket'
  sock.close()
