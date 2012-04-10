import Queue, random, hashlib
import server, easy_client

###############################################################

#   CIS 598 Senior Project by Brian Cain

#   bccain@ksu.edu

#   node.py - Code for node class

###############################################################

""" Todo:
      * ID != Sequence Number
      * Node will have dictionary of Queues, key = Destination ID, Value = Queue of route tokens
      * Interprocess communication, with only forward flooding working
        - Intermediates will keep track of: Prev hop, next hop, and sequence num
        - Send objects over python by using pickling
      * Look up ipython
"""

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
"""

def flood_network(neighbor_list):
  for n in neighbor_list:
    pass
  pass

def main():
  pass

############################################
# Node Class
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

    # Init listening server
    self.serv = server.server(self.DHT_ID, True)
    print self.serv
    # begin listening for incoming connections on port number
    # self.serv.run_server()

    # Init node as client
    self.client = easy_client.client(self.DHT_ID, False)
    print self.client, "\n"

# Membership & Invitation Authority will initiate flooding technique
  def flood(self):
    # sequence number
    seq_numz = self.z + 10000
    disco_msg = (seq_numz, self.scope, self.IBE)
    print "Discovery Message: ", disco_msg
    return disco_msg

  def am_I_the_dest(self, msg):
    if msg[2][2] == 6 and 6 == self.DHT_ID: return True
    return False

  # call before figuring out which class I need to use
  # during the flood
  def am_I_the_node(self, dest_id):
    if dest_id == self.DHT_ID: 
      return True
    else:
      print "Nope.avi"
      return False
    
  # discovery message, and source
  def process_message(self, disco_msg, source) :
    # adds to dictionary for ids not dealth with

    # implicit can I decrypt, if ID = 6
    if self.am_I_the_node(disco_msg[2][2]):
      print "Destination Node. You've reached the destination"
    else :
      pass
      # keep track of previous hop, next hop, and sequence num
      # previous hop = source
      # next hop(s) = physical neighbors
      # sequence num = disco_msg[0]
      # for n in physical_neighbors:
      #   n.flood()

  def who_am_i(self):
    return self.DHT_ID

  def set_neighbors(self, neigh_list):
    self.neighbor_list = neigh_list

####################################
# Will Run Main
####################################
if __name__ == '__main__':
  main()
