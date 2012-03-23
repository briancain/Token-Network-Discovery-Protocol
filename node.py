import Queue
import random

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
  if msg_DHT_ID == 11:
    return True

# flooding network will probably be pushed do different function later
def flood_network(source) :
  print "Flood ID: ", source.msg_DHT_ID

  return None

############################################
# Source node, responsible for flooding
############################################
class node_Source:
  def __init__(self, dht_id):
    print "      Source node initialized!"
    self.msg_DHT_ID =  dht_id # id of node, will be of form h(h(z)) later
    self.scope = 6 # flood depth, is this given?
    z = random.randint(1, 10) # random number
    R = 0 # R is route descriptor, will be random bit-string of some fixed size later
    self.IBE_prefix = [z, R] 
    # Can only talk to neighbors (Array/List of DHT keys)
    self.neighbor_list = [] # Just an example for now, list with DHT key
    # Private routing Token -> An array of token strings which is built after flooding, which will be padded with the queue
    # Needs to be a hash table (key=DHT ID, value =routing token)
    self.prt = dict([]) # of the form [('me': d, z), ('me': y, w),...] after initialized (dictionary)

# Membership & Invitation Authority will initiate flooding technique
  def flood(self, neigh):
    print "\nFlooding network...."
    self.prt = flood_network(neigh) # this function will probably return the routing tables

  def who_am_i(self):
    return self.msg_DHT_ID

############################################################
# Intermediate Node class
# - Will pad route token with queue
# - Cannot decrypt route discovery request, so intermediate
############################################################
class node_Int:
  def __init__(self, dht_id, req_id, source) :
    print "     Intermediate node initialized!"
    self.msg_DHT_ID = dht_id # place holder value for now
    self.queue = Queue.Queue() # Queue which can pad token
    self.prt = dict([('1', [2,3,4])]) # example of private route token being sent back
    self.request_id = req_id # Request ID
    self.source = source # source of request, must keep all

    # generate padded queue
    #for i in range(7):
    #  self.pad_q.put(None)

  def send_message(self, queue_route) :
    # adds self to route
    queue_route.put(self.msg_DHT_ID)
    return queue_route

  def who_am_i(self):
    return self.msg_DHT_ID

##############################################################################
# Destination node, going to be asked if it's correct node in flooding
# algorithm
##############################################################################
class node_Dest:
  def __init__(self, dht_id) :
    print "     Destination node initialized!"
    self.msg_DHT_ID = dht_id # dummy value for ID'
    self.prt = dict([('1', [2,3,4])]) # example prt to send back

  def check_node(self, msg_queue) :
    # if this is the node we are looking for....
    if am_I_the_node(self.msg_DHT_ID):
      print "You are the winner!"
      # since Dest node can decrypt msg, generate DH half-key and compose response
      # message = [self.msg_DHT_ID, self.prt, msg_queue] # then place on Queue?
      q = Queue.Queue()
      q.put(msg_DHT_ID)
      return q # returning a response message
    else :
      print "These are not the nodes you are looking for"

  def who_am_i(self):
    return self.msg_DHT_ID
