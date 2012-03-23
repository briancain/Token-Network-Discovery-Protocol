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

def flood_network() :
  print "<<-Not Implemented->>"

############################################
# Source node, responsible for flooding
############################################
class node_Source:
   def __init__(self):
     print "      Source node initialized!"
     self.msg_DHT_ID = 1 # id of node, will be of form h(h(z)) later
     self.MIA_flood = False # will have to get a signal from MIA to start flooding
     self.scope = 6 # flood depth, is this given?
     z = random.randint(1, 10) # random number
     R = 0 # R is route descriptor, will be random bit-string of some fixed size later
     self.IBE_prefix = [z, R] 
    # Can only talk to neighbors (Array/List of DHT keys)
    # Is the physical neighbors given to us? It has to know what its physical
    # neighbors are if it wants to flood, so I assume so
     self.neighbor_list = [2, 3, 4, 5, 6] # Just an example for now, list with DHT key
    # Private routing Token -> An array of token strings which is built after flooding, which will be padded with the queue
    # Needs to be a hash table (key=DHT ID, value =routing token)
     self.prt = dict([]) # of the form [('me': d, z), ('me': y, w),...] after initialized (dictionary)
    
# Membership & Invitation Authority will initiate flooding technique
   def flood(self):
     print "Flooding network...."
     self.prt = flood_network() # this function will probably return the routing tables

   def who_am_i(self):
     return self.msg_DHT_ID

############################################################
# Intermediate Node class
# - Will pad route token with queue
# - Cannot decrypt route discovery request, so intermediate
############################################################
class node_Int:
  def __init__(self, req_id, source) :
    print "     Intermediate node initialized!"
    self.msg_DHT_ID = 5 # place holder value for now
    self.pad_q = Queue.Queue() # Queue which can pad token
    self.prt = dict([('1', [2,3,4])]) # example of private route token being sent back
    self.request_id = req_id # Request ID
    self.source = source # source of request, must keep all

    # generate padded queue
    for i in range(7):
      self.pad_q.put(None)

  # Must pad message, but how does it add its own ID to the hash table?
  # When padding a dictionary/hash table, it will just go has a key/value, or am I wrong?
  # Maybe the route needs to be padded in the key/value? Not sure
  def send_message(self) :
    # Adds empty queue to dictionary
    self.prt['None'] = self.pad_q
    # adds self to route
    self.prt['1'].append(self.msg_DHT_ID)
    return self.prt

  def who_am_i(self):
    return self.msg_DHT_ID

##############################################################################
# Destination node, going to be asked if it's correct node in flooding
# algorithm
##############################################################################
class node_Dest:
  def __init__(self, z, prefix, route, gx) :
    print "     Destination node initialized!"
    self.msg_DHT_ID = 11 # dummy value for ID'
    self.prt = dict([('1', [2,3,4])]) # example prt to send back
    
  def check_node(self, msg_queue) :
    # if this is the node we are looking for....
    if am_I_the_node(self.msg_DHT_ID):
      print "You are the winner!"
      # since Dest node can decrypt msg, generate DH half-key and compose response
      message = [self.msg_DHT_ID, self.prt, msg_queue] # then place on Queue!
      return message # returning a response message
    else :
      print "These are not the nodes you are looking for"

  def who_am_i(self):
    return self.msg_DHT_ID
