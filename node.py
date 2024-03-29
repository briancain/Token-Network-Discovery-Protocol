import random, collections, xmlrpclib, multiprocessing, logging
from collections import deque
from multiprocessing import Queue

###############################################################

#   CIS 598 Senior Project by Brian Cain

#   bccain@ksu.edu

#   node.py - Code for node class

###############################################################

""" Todo:
      * Construct Route Tokens
      * Check for accuracy
"""

def main():
  pass

############################################
# Node Class
############################################
class node:
  # def __init__(self, dht_id, q, q2):
  def __init__(self, dht_id):
    self.DHT_ID =  dht_id # id of node
    # Can only talk to neighbors (Array/List of DHT keys)
    self.neighbor_list = [] # Just an example for now, list with node neighbors
    # Private routing Token -> A queue of token strings which is built after flooding, which will be padded with the null-queue
    # Needs to be a hash table (key=DHT ID, value =routing token)
    self.dups = dict()

    if self.DHT_ID is 1: # could be ==, since they will both be holding the value 6, rather than an instance
      self.scope = 8 # flood depth
      self.R = deque() # route descriptor
      self.z = random.randint(1001, 1010) # random number
      self.IBE = (self.z, self.R, 6) # object to say if node is DHT node we're looking for
      self.route_queue = deque()

  def __str__(self): return str(self.DHT_ID)

  # special print for node
  # will print node ID before message to make it clear which process is printing to stdout
  def bprint(self, *args): print "[Node", self, "] ", " ".join([str(x) for x in args])

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
    # disco_msg_test = self.msg_coll(seqnum=seq_numz, scope=self.scope, ibe=self.IBE)
    self.bprint("Discovery Message:", disco_msg)

    for n in self.neighbor_list:
      self.bprint("Sending discovery message:", disco_msg, "to NodeID: ", n.DHT_ID)
      # will process message over network here
      self.from_me_queue.put((n.DHT_ID, self.DHT_ID, disco_msg))

  # runs the node
  # parses the message from the communication Queues
  def run_node(self, nid, q, q2):
  # def run_node(self, nid):
    self.to_me_queue = q
    self.from_me_queue = q2
    while True:
      m = self.to_me_queue.get() #this DOES block
      if m == "STOP": return
      elif m == "FLOOD":
        self.bprint("Will now flood")
        self.flood()
      elif m[0] == "LIST":
        self.bprint("Setting Neighbors", m[1])
        self.set_neighbors(m[1])
      elif m[0] == "CONSTRUCT":
        self.bprint("Constructing Route Tokens")
        # "CONSTRUCT", source id, queue
        source = m[1]
        que = m[2]
        self.construct_token(que, source) 
      else: # flooding network
        msg, prev_hop = m
        self.process_message(msg, prev_hop)

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

  # does the given key exist within dups?
  def is_dups(self, prev_hop, dht_id):
    if (prev_hop, dht_id) in self.dups:
      return True
    else :
      return False

  # discovery message, and source
  def process_message(self, disco_msg, prev_hop) :
    # adds to dictionary for ids not dealth with
    # implicit can I decrypt, if ID = 6

    # decrease scope by 1, if 0 drop message
    self.bprint("Node:", self.DHT_ID, " in process message ", "With scope:", disco_msg[1])
    if disco_msg[1] < 1:
      self.bprint("Scope is 0, dropping message...")
      exit() # temp fix
      return
    else :
      # Decrease scope and continue on
      disco_msg[1] -= 1
      self.bprint("Disco Message is after Decrease in Scope:", disco_msg)

      if self.am_I_the_dest(disco_msg):
        """
          The flood has reached the destination, and will begin
          sending back to construct tokens here.

          Send message to all of destinations neighbors to start looking at dupes
        """
        self.bprint("\n\n\n\n\n\n\n\n\n\nDestination Node. You've reached the destination")
        que = deque()
        que.append(self.DHT_ID)
        #self.construct_token(que, self.DHT_ID)
        for n in self.neighbor_list:
          msg = ["CONSTRUCT", n.DHT_ID, self.DHT_ID, que]
          self.from_me_queue.put(msg)

      else :
        self.bprint("I am not the destination, going to process message")
        """
          For each neighbor within the list
            add duplicate sequence number
            do not flood disco_msg to node where it came from
            Otherwise, add prevhop+nexthop into dictionary and continue flooding
        """
        for n in self.neighbor_list:
          self.bprint("Within process message, looking at neighbor node id:", n.DHT_ID)
          # if not self.dups_seqnums: self.dups_seqnums = dict() # the same thing?
          try:
            self.dups_seqnums[disco_msg[0]] = True
          except:
            self.dups_seqnums = dict()
            self.dups_seqnums[disco_msg[0]] = True

          if n.DHT_ID is prev_hop: 
            self.bprint("Neighbor DHT_ID == Previous Hop...continuing on...")
            continue # don't flood source with same message
          else :
            if not self.is_dups(prev_hop, n.DHT_ID):
              self.bprint("Not a dup, Flooding neighbor", n.DHT_ID)
              self.dups[(prev_hop, n.DHT_ID)] = True
              self.bprint("Added dupes to dictionary", self.dups)
              ###ASSUME NEXT_HOP is n??? or vice versa?
              self.from_me_queue.put((n.DHT_ID, self.DHT_ID, disco_msg))
            else:
              self.bprint("Got dupe ", n.DHT_ID, " ", disco_msg, ", not flooding...")

  # constructs route tokens
  def construct_token(self, que, source):
    """
      Constructs tokens after flooding has completed
      If source, add the queue token to the route_token queue
      Otherwise, look at each key within dups, and construct token with self.id and send it to dup id
    """
    self.bprint("We are in construct token")
    if self.DHT_ID is 1:
      self.route_queue.append(que)
      self.bprint("We have reached the source, adding token to Queue...", self.route_queue)
    else:
      #for n in self.neighbor_list:
      self.bprint("Not the source, trying to send message to keys", self.dups)
      # this is not evaluating
      for key in self.dups: #(prev_hop, next_node_id) = True
        """
          for keys in dictionary: #(prev_hop, next_node_id) = True
            send queue to node
        """
        self.bprint("Looking at keys:", key)
        if key[1] is source: # is this needed or ever reached?
          self.bprint("Don't send construction back...continuing on...")
          continue
        elif self.dups[key] is False:
          continue
        else:
          # maybe debug here to see what keys are what in dictionary
          self.bprint("Sending route token to neighbors:", key[0])
          que.append(self.DHT_ID)
          self.bprint("Added to queue:", que)
          msg = ["CONSTRUCT", key[0], self.DHT_ID, que]
          self.dups[key] = False
          self.from_me_queue.put(msg)

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
