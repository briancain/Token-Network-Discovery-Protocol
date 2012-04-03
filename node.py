import Queue, random, hashlib

###############################################################

#   CIS 598 Senior Project by Brian Cain

#   bccain@ksu.edu

#   node.py - Code for node class

###############################################################

""" Todo:
        - Interprocess communication
          o With sockets?
        - Merge nodes into one class
"""

# simple def for checking if dest is right node (for now...)
def am_I_the_node(msg_DHT_ID):
  if msg_DHT_ID == 6:
    return True

# flooding network will probably be pushed do different function later
"""def flood_network(source) :
  # needs to be changed for who am i node function
  print "# Flood ID: ", source.msg_DHT_ID
  if am_I_the_node(source.msg_DHT_ID) :
    print "Destination node found!"
    q = source.check_node()
    return q
  else :
    print "# Not destination node\n"
    return False

  return None
"""

def flood_network(neighbor_list):
  for n in neighbor_list:
    pass
  pass

############################################
# Source node, responsible for flooding
############################################
class node_Source:
  def __init__(self, dht_id):
    self.msg_DHT_ID =  dht_id # id of node, will be of form h(h(z)) later
    self.scope = 2 # flood depth
    self.gx = None # key/ignore
    self.R = None # route descriptor
    self.z = random.randint(1, 10) # random number
    self.IBE = (self.z, self.R) # object to say if node is DHT node we're looking for
    # Can only talk to neighbors (Array/List of DHT keys)
    self.neighbor_list = [] # Just an example for now, list with node neighbors
    # Private routing Token -> A queue of token strings which is built after flooding, which will be padded with the null-queue
    self.private_route_q = Queue.Queue() # queue for holding private route tokens, form [[x,y,z],...]
    self.token_dict = dict([]) # a dictionary of Queues

# Membership & Invitation Authority will initiate flooding technique
  def flood(self):
    disco_msg = (self.msg_DHT_ID, self.scope, self.gx, self.IBE)
    print "Discovery Message: ", disco_msg
    # route_token = flood_network(source) 
    # self.private_route_q.put(route_token)

  def who_am_i(self):
    return self.msg_DHT_ID

  def set_neighbors(self, neigh_list):
    self.neighbor_list = neigh_list

############################################################
# Intermediate Node class
# - Will pad route token with queue
# - Cannot decrypt route discovery request, so intermediate
############################################################
class node_Int:
  def __init__(self, dht_id, req_id) :
    self.msg_DHT_ID = dht_id # place holder value for now
    # Needs to be a hash table (key=DHT ID, value =routing token)
    self.dupe = dict([]) # hash table indexed by id and route
    self.response = dict([])
    self.request_id = req_id # Request ID
    # self.source = source # source of request, must keep all
    self.neighbor_list = []

    # generate padded queue
    #for i in range(7):
    #  self.pad_q.put(None)

  # discovery message, request ID and physical neighbor from disco_message
  def send_message(self, disco_msg, route_id, source) :
    # adds to dictionary for ids not dealth with
    if route_id not in self.dupe:
      # it's a duplicate -- do nothing
      return

    if route_id in self.response:
      # reply to something we've seen before
      # self.response[route_id] = return_hop
      # forward_message to return_hop
      pass
    else :
      responses[route_id] = source
      # decrease scope by 1
      # forward_message to all neighbors who are not source

  def flood(self, source) :
    # generating routing token
    temp_list = flood_network(source)
    temp_list.append(self.msg_DHT_ID)
    return temp_list

  def who_am_i(self):
    return self.msg_DHT_ID

  def set_neighbors(self, neigh_list):
    self.neighbor_list = neigh_list

##############################################################################
# Destination node, going to be asked if it's correct node in flooding
# algorithm
##############################################################################
class node_Dest:
  def __init__(self, dht_id) :
    self.msg_DHT_ID = dht_id # dummy value for ID'

 # discovery message, request ID and physical neighbor from disco_message
  def check_node(self, disco_msg, route_id, source) :
    # if this is the node we are looking for....
    # target keeps track of z, prefix, route, and g^x
    IBE = disco_msg[3]
    z = IBE[0]
    R = IBE[1]
    scope = disco_msg[1]

    # if scope is 0, drop message
    if scope == 0 :
      return

    print "You are the winner!\n"
    lst = [self.msg_DHT_ID]
    return lst # returning a response message

  def who_am_i(self):
    return self.msg_DHT_ID

  def set_neighbors(self, neigh_list):
    self.neighbor_list = neigh_list
