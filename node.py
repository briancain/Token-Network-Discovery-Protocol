import Queue, random, hashlib, collections
import server, client, errno
from collections import deque

###############################################################

#   CIS 598 Senior Project by Brian Cain

#   bccain@ksu.edu

#   node.py - Code for node class

###############################################################

""" Todo:
      * Interprocess communication, with only forward flooding working
        - Intermediates will keep track of: Prev hop, next hop, and sequence num
       - Send objects over python by using pickling, or perhaps json
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

def main():
  pass

############################################
# Node Class
############################################
class node:
  def __init__(self, dht_id):
    self.DHT_ID =  dht_id # id of node
    # Can only talk to neighbors (Array/List of DHT keys)
    self.neighbor_list = [] # Just an example for now, list with node neighbors
    # Private routing Token -> A queue of token strings which is built after flooding, which will be padded with the null-queue
    self.routing_table = dict() # a dictionary of Queues, key = dest id
    # Needs to be a hash table (key=DHT ID, value =routing token)
    self.prev_hops = dict() # hash table indexed by id and route
    self.response = dict()
    self.msg_coll = collections.namedtuple('msg_coll', 'seqnum scope ibe')

    # is not??
    if self.DHT_ID is 1: # could be ==, since they will both be holding the value 6, rather than an instance
      self.scope = 8 # flood depth
      self.R = deque() # route descriptor
      self.z = random.randint(1001, 1010) # random number
      self.IBE = (self.z, self.R, 6) # object to say if node is DHT node we're looking for

    self.flood_flag = False

    # Init listening server
    # self.serv = server.server(self.DHT_ID, True)
    # print "[Node ", self.DHT_ID, "] ", self.serv
    # begin listening for incoming connections on port number
    # self.serv.run_server()

    # Init node as client
    #self.client_list = []
    # self.client = client.client(self.DHT_ID, False)

    # self.client2 = client.client(100000, True)

    #try:
    #  self.client2 = client.client(10100, True)
    #except:
    #  print "!!!!! - [Node ", self.DHT_ID, "] ", "gaierror: [Errno 8] nodename nor sername provided, or not known !!!!!"
    #
    #""" Linux only, does not work on OS X
    #try:
    #  self.client2 = client.client(10100, True)
    #except client.socket.error as e:
    #  if e.errno == errno.ECONNREFUSED:
    #    print "[Node ", self.DHT_ID, "] ", "Connection Refused"
    #  else:
    #    raise
    #"""

    """print "[Node ", self.DHT_ID, "] ", self.client, "\n"
    print self
    print self, self.client, "\n"
    self.bprint("hi", self.client, "\n\n\n")
    """

  def __str__(self): return str(self.DHT_ID)

  def bprint(self, *args): print self, " ".join([str(x) for x in args])

  # Begin listening for incoming connections
  def begin_listen(self):
    print "[Node ", self.DHT_ID, "] ", self.serv
    # begin listening for incoming connections on port number
    self.serv.run_server()

  # Membership & Invitation Authority will initiate flooding technique
  def flood(self):
    #if self.flood_flag == True:
    #  # has already flooded its neighbors
    #  return
    if self.DHT_ID is not 1:
      raise Exception, "Not a valid node for flooding, sorry"
      return

    print "[Node ", self.DHT_ID, "] ", "Flooding..."
    #self.flood_flag = True
    # sequence number
    seq_numz = self.z + 10000
    disco_msg = [seq_numz, self.scope, self.IBE] # only built by source
    # use this disco msg instead for later
    disco_msg_test = self.msg_coll(seqnum=seq_numz, scope=self.scope, ibe=self.IBE)
    print "[Node ", self.DHT_ID, "] ", "Discovery Message: ", disco_msg
    return disco_msg
    """for n in self.neighbor_list:
      print "Node ", self.DHT_ID, " sending disco_msg: ", n.DHT_ID
      # will process message over network here
      n.process_message(disco_msg, self.DHT_ID)
    """

  # Is this node the destination?
  def am_I_the_dest(self, msg):
    if msg[2][2] is 6 and 6 is self.DHT_ID: return True
    return False

  # call before figuring out which class I need to use
  # during the flood
  def am_I_the_node(self, dest_id):
    if dest_id is self.DHT_ID: 
      return True
    else:
      return False
    
  # discovery message, and source
  def process_message(self, disco_msg, prev_hop) :
    # adds to dictionary for ids not dealth with
    # implicit can I decrypt, if ID = 6

    # decrease scope by 1, if 0 drop message
    if disco_msg[1] <= 0:
      return
    else :
      disco_msg[1] -= 1

    if self.am_I_the_dest(disco_msg):
      print "Destination Node. You've reached the destination"
      return
    else :
      # keep track of previous hop, next hop, and sequence num
      ###self.prev_hop[disco_msg[0]] = prev_hop # Save this for dupe
      ###self.next_hops[disco_msg[0]] = self.neighbor_list # next hop = physical neig, dictionary
      ###sequence_num = disco_msg[0] # should not be a single variable
      # see if these variables match a previous message within dupe
      # otherwise don't flood
      for n in self.neighbor_list:
        if not self.dups_seqnums: self.dups_seqnums = dict()
        self.dups_seqnums[disco_msg[0]] = True
        if not self.dups: self.dups_seqnums = dict()
        if n.DHT_ID == prev_hop: # this might be changed to an is if prev hop and DHT_ID are the same instance, rather than the same variable
          # don't flood source with same message
          continue
        else :
          if not check_dups(disco_msg, prev_hop):
            print "Node ", self.DHT_ID, " flooding: ", n.DHT_ID
            ###FIXME???????
            self.dups[(prev_hop, next_hop)] = True
            ###ASSUME NEXT_HOP is n??? or vice versa?
            n.process_message(disco_msg, self.DHT_ID)
          else:
            print "Node ", self.DHT_ID, " got dup ", disco_msg, ", not flooding"

  # Return id of node
  def who_am_i(self):
    return self.DHT_ID

  # Set neighbors of node
  def set_neighbors(self, neigh_list):
    self.neighbor_list = neigh_list

####################################
# Will Run Main
####################################
if __name__ == '__main__':
  main()
