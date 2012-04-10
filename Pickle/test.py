import time
import pickle
import socket, sys
import pprint

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = sys.argv.pop() if len(sys.argv) == 3 else '127.0.0.1'
PORT = 1060

if sys.argv[1:] == ['server']:

  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((HOST, PORT))
  s.listen(1)

  print 'Listening at', s.getsockname()

  sc, sockname = s.accept()

  print 'Accepted connection from', sockname

  sf = sc.makefile( "rb" )

  length_list = []
  while True:
    char = sf.read(1)
    if char == '\n':
      break
    else:
      length_list.append(int(char))
      length = 0
      for digit in length_list:
        length = length * 10 + digit
        data = sf.read(length)

      d = pickle.load(data)

      pprint.pprint(d)

      sc.shutdown(socket.SHUT_RDWR)
      sc.close()
      s.close()

elif sys.argv[1:] == ['client']:

  s.connect((HOST, PORT))
  # s.shutdown(socket.SHUT_RD)

  d = dict()

  d[ 'Name' ] = 'Jake Thompson.'
  d[ 'Age' ] = 25
  d[ 'Location' ] = 'Washington, D.C.'

  sf = s.makefile( "wb" )

  string = pickle.dumps( d, pickle.HIGHEST_PROTOCOL )
  sf.write('%d\n' % len(string))
  sf.write(string)
  sf.flush()

  #time.sleep(10)
  sf.close()
  s.shutdown(socket.SHUT_RDWR)
  # s.close()

else:
  print >>sys.stderr, 'usage: streamer.py server|client [host]'
