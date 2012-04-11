import xmlrpclib

proxy = xmlrpclib.ServerProxy("http://localhost:8000/")
with open("python_logo.jpg", "wb") as handle:
      handle.write(proxy.python_logo().data)
