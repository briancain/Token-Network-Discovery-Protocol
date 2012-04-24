import Queue, random, collections, xmlrpclib, multiprocessing, logging
from collections import deque
from SimpleXMLRPCServer import SimpleXMLRPCServer

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
    self.dups = dict()
    self.response = dict()
    self.msg_coll = collections.namedtuple('msg_coll', 'seqnum scope ibe')

    # is not??
    if self.DHT_ID is 1: # could be ==, since they will both be holding the value 6, rather than an instance
      self.scope = 8 # flood depth
      self.R = deque() # route descriptor
      self.z = random.randint(1001, 1010) # random number
      self.IBE = (self.z, self.R, 6) # object to say if node is DHT node we're looking for

    """print "[Node ", self.DHT_ID, "] ", self.client, "\n"
    print self
    print self, self.client, "\n"
    self.bprint("hi", self.client, "\n\n\n")
    """

    """jobs = []
    ran = len(self.neighbor_list)
    self.port_list, self.server_list = self.init_server(ran)
    self.client_list = self.init_clients(ran)
    multiprocessing.log_to_stderr()
    self.logger = multiprocessing.get_logger()
    self.logger.setLevel(logging.INFO)
    for i in range(0, ran):
      ser = self.server_list[i]
      pids = self.port_list[i]
      p = multiprocessing.Process(target=self.begin_listen, args=(ser, pids))
      jobs.append(p)
      p.start()
    """

  def __str__(self): return str(self.DHT_ID)

  def bprint(self, *args): print "[Node ", self, "] ", " ".join([str(x) for x in args])

  def init_clients(self, ran):
    c_list = []
    for s in range(0, ran):
      port = ((self.neighbor_list[s])*4000) + self.DHT_ID
      st = "http://localhost:" + str(port) + "/"
      client = xmlrpclib.ServerProxy(st)
      c_list.append(client)

    return c_list

  def init_server(self, ran):
    p_list = []
    s_list = []
    for s in range(0, ran):
      # port = 8000 + self.DHT_ID + (s+100)
      port = (self.DHT_ID*4000) + self.neighbor_list[s]
      p_list.append(port)

      server = SimpleXMLRPCServer(("localhost", port))
      server.register_multicall_functions()
      server.register_function(self.process_message, "process_message")
      s_list.append(server)

    return p_list, s_list

  # Begin listening for incoming connections
  def begin_listen(self, server, port_id):
    print "[Node ", self.DHT_ID, "] ", "Listening on", port_id, "....."
    server.serve_forever()

  # Membership & Invitation Authority will initiate flooding technique
  def flood(self):
    if self.DHT_ID is not 1:
      raise Exception, "Not a valid node for flooding, sorry"
      return

    self.bprint("Starting Flood!!!!!")
    # sequence number
    seq_numz = self.z + 10000
    disco_msg = [seq_numz, self.scope, self.IBE] # only built by source
    # use this disco msg instead for later
    disco_msg_test = self.msg_coll(seqnum=seq_numz, scope=self.scope, ibe=self.IBE)
    self.bprint("Discovery Message:", disco_msg)
    # for each client in node, process message
    # print "Client List:", self.client_list
    """for c in self.client_list:
      multicall = xmlrpclib.MultiCall(c)
      print "\n\nClient:", c
      multicall.process_message(disco_msg, self.DHT_ID)
    """ 

    # use multi-process here????, shared memory of dups?????
    for n in self.neighbor_list:
      self.bprint("sending discovery message:", disco_msg, "to NodeID: ", n.DHT_ID)
      # will process message over network here
      n.process_message(disco_msg, self.DHT_ID)  

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
    
  def check_dups(self, disco_msg, prev_hop):
    pass

  # discovery message, and source
  def process_message(self, disco_msg, prev_hop) :
    # adds to dictionary for ids not dealth with
    # implicit can I decrypt, if ID = 6
    # decrease scope by 1, if 0 drop message
    self.bprint("Node:", self.DHT_ID, " in process message...")
    if disco_msg[1] <= 0:
      return
    else :
      disco_msg[1] -= 1

    if self.am_I_the_dest(disco_msg):
      bprint("Destination Node. You've reached the destination")
      return
    else :
      # keep track of previous hop, next hop, and sequence num
      ###self.prev_hop[disco_msg[0]] = prev_hop # Save this for dupe
      ###self.next_hops[disco_msg[0]] = self.neighbor_list # next hop = physical neig, dictionary
      ###sequence_num = disco_msg[0] # should not be a single variable
      # see if these variables match a previous message within dupe
      # otherwise don't flood
      for n in self.neighbor_list:
        self.bprint("Within process message, looking at neighbor node id:", n.DHT_ID)
        if not self.dups_seqnums: self.dups_seqnums = dict() # the same thing?
        self.dups_seqnums[disco_msg[0]] = True
        if bool([a for a in self.dups.values() if a != []]): self.dups_seqnums = dict() # the same thing?
        if n.DHT_ID is prev_hop: # this might be changed to an is if prev hop and DHT_ID are the same instance, rather than the same variable
          continue # don't flood source with same message
        else :
          if not self.check_dups(disco_msg, prev_hop):
            self.bprint("Flooding neighbor", n.DHT_ID)
            ###FIXME???????
            self.dups[(prev_hop, n)] = True
            ###ASSUME NEXT_HOP is n??? or vice versa?
            n.process_message(disco_msg, self.DHT_ID)
          else:
            self.bprint("Got dupe ", disco_msg, ", not flooding...")

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
