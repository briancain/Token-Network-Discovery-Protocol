import Queue, random, hashlib

###############################################################

#   CIS 598 Senior Project by Brian Cain

#   bccain@ksu.edu

#   node.py - Code for node class

###############################################################

""" Todo:
      * Merge node classes into one overall class 10 
      * ID != Sequence Number
      * Node will have dictionary of Queues, key = Destination ID, Value = Queue of route tokens
      * Interprocess communication, with only forward flooding working
        - Intermediates will keep track of: Prev hop, next hop, and sequence num
        - Send objects over python by using pickling
      * Look up ipython
"""


 # call before figuring out which class I need to use
  # during the flood
#def am_I_the_node(self, msg):
##CAN I DECRYPT THE NEXT ROUTE TOKEN?
#    if msg[2][2] = self.DHT_ID: return True
#    return False

def am_I_the_dest(self, msg):
  if msg[2][2] == 6 and 6 == self.DHT_ID: return True
  return False

def flood_network(neighbor_list):
  for n in neighbor_list:
    pass
  pass

############################################
# Source node, responsible for flooding
############################################
class node:
  def __init__(self, dht_id):
    self.DHT_ID =  dht_id # id of node
    self.scope = 8 # flood depth
    self.R = Queue.Queue() # route descriptor
    self.z = random.randint(1001, 1010) # random number
    self.IBE = (self.z, self.R, 6) # object to say if node is DHT node we're looking for
    # Can only talk to neighbors (Array/List of DHT keys)
    self.neighbor_list = [] # Just an example for now, list with node neighbors
    # Private routing Token -> A queue of token strings which is built after flooding, which will be padded with the null-queue
    self.routing_table = dict() # a dictionary of Queues, key = dest id
    # Needs to be a hash table (key=DHT ID, value =routing token)
    self.dupe = dict() # hash table indexed by id and route
    self.response = dict()

# Membership & Invitation Authority will initiate flooding technique
  def flood(self):
    seq_numz = self.z + 10000
    disco_msg = (seq_numz, self.scope, self.IBE)
    print "Discovery Message: ", disco_msg
    return disco_msg

  def am_I_the_dest(self, msg):
    if msg[2][2] == 6 and 6 == self.DHT_ID: return True
    return False

  # call before figuring out which class I need to use
  # during the flood
  def am_I_the_node(msg):
    if msg[2][2] == self.DHT_ID: return True
    return False

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

# discovery message, request ID and physical neighbor from disco_message
  def process_message(self, disco_msg, source) :
    # adds to dictionary for ids not dealth with

    # implicit can I decrypt, if ID = 6
    if am_I_the_node(disco_msg[2][2]):
      return

  def reply(self, route_request, scope):
    # if it can decrypt route_request, generate gk-half key (ignore) and compose a response
    ID_prime = None # seq_number_2

    # R = FIFO queue with max entires
    # each entry can read Null (None)
    response = (ID_prime, R)
    scope = scope - 1
    # sends message to D, and "floods original request"
    return response, scope

  def who_am_i(self):
    return self.DHT_ID

  def set_neighbors(self, neigh_list):
    self.neighbor_list = neigh_list

############################################################
# Intermediate Node class
# - Will pad route token with queue
# - Cannot decrypt route discovery request, so intermediate
############################################################
class node_Int:
  def __init__(self, dht_id, req_id) :
    self.DHT_ID = dht_id # place holder value for now
    # Needs to be a hash table (key=DHT ID, value =routing token)
    self.dupe = dict() # hash table indexed by id and route
    self.response = dict()
    self.R = Queue.Queue()
    self.request_id = req_id # Request ID
    # self.source = source # source of request, must keep all
    self.neighbor_list = []

    # generate padded queue
    for i in range(7):
      self.R.put(None)

  # discovery message, request ID and physical neighbor from disco_message
  def process_message(self, disco_msg, source) :
    # adds to dictionary for ids not dealth with

    # implicit can I decrypt, if ID = 6
    if am_I_the_node(disco_msg[2][2]):
      return

  # call before figuring out which class I need to use
  # during the flood
  def am_I_the_node(msg):
    if msg[2][2] == self.DHT_ID: return True
    return False

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

  def reply(self, route_request, scope):
    # if it can decrypt route_request, generate gk-half key (ignore) and compose a response
    ID_prime = None # seq_number_2

    # R = FIFO queue with max entires
    # each entry can read Null (None)
    response = (ID_prime, R)
    scope = scope - 1
    # sends message to D, and "floods original request"
    return response, scope

  def flood(self, source) :
    # generating routing token
    temp_list = flood_network(source)
    temp_list.append(self.msg_DHT_ID)
    return temp_list

  def who_am_i(self):
    return self.DHT_ID

  def set_neighbors(self, neigh_list):
    self.neighbor_list = neigh_list

##############################################################################
# Destination node, going to be asked if it's correct node in flooding
# algorithm
##############################################################################
class node_Dest:
  def __init__(self, dht_id) :
    self.DHT_ID = dht_id # dummy value for ID'

 # discovery message, request ID and physical neighbor from disco_message
  def check_node(self, disco_msg, route_id, source) :
    # if this is the node we are looking for....
    # looks up table from previous request IDs
    # finds the next hop, where response must be sent

    # if scope is 0, drop message
    if scope == 0 :
      return

    print "You are the winner!\n"
    # constructs route token
    lst = [self.msg_DHT_ID]
    return lst # returning a response message

  def who_am_i(self):
    return self.DHT_ID

  def set_neighbors(self, neigh_list):
    self.neighbor_list = neigh_list
