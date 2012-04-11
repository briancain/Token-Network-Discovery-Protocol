import xmlrpclib

proxy = xmlrpclib.ServerProxy("http://localhost:8000/")
try:
  proxy.add(2, 5)
except xmlrpclib.Fault, err:
  print "A fault occurred"
  print "Fault code: %d" % err.faultCode
  print "Fault string: %s" % err.faultString
