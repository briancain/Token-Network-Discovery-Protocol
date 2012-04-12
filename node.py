import Queue, random, hashlib
import server, client

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
    self.scope = 8 # flood depth
    self.R = Queue.Queue() # route descriptor
    self.z = random.randint(1001, 1010) # random number
    self.IBE = (self.z, self.R, 6) # object to say if node is DHT node we're looking for
    # Can only talk to neighbors (Array/List of DHT keys)
    self.neighbor_list = [] # Just an example for now, list with node neighbors
    # Private routing Token -> A queue of token strings which is built after flooding, which will be padded with the null-queue
    self.routing_table = dict() # a dictionary of Queues, key = dest id
    # Needs to be a hash table (key=DHT ID, value =routing token)
    self.prev_hops = dict() # hash table indexed by id and route
    self.response = dict()

    self.flood_flag = False

    # Init listening server
    self.serv = server.server(self.DHT_ID, True)
    print "[Node ", self.DHT_ID, "] ", self.serv
    # begin listening for incoming connections on port number
    # self.serv.run_server()

    # Init node as client
    self.client = client.client(self.DHT_ID, False)
    print "[Node ", self.DHT_ID, "] ", self.client, "\n"

# Membership & Invitation Authority will initiate flooding technique
  def flood(self):
    if self.flood_flag == True:
      # has already flooded its neighbors
      return

    print "[Node ", self.DHT_ID, "] ", "Flooding..."
    self.flood_flag = True
    # sequence number
    seq_numz = self.z + 10000
    disco_msg = [seq_numz, self.scope, self.IBE] # only built by source
    print "[Node ", self.DHT_ID, "] ", "Discovery Message: ", disco_msg
    for n in self.neighbor_list:
      print "Node ", self.DHT_ID, " sending disco_msg: ", n.DHT_ID
      # will process message over network here
      n.process_message(disco_msg, self.DHT_ID)

  def am_I_the_dest(self, msg):
    if msg[2][2] == 6 and 6 == self.DHT_ID: return True
    return False

  # call before figuring out which class I need to use
  # during the flood
  def am_I_the_node(self, dest_id):
    if dest_id == self.DHT_ID: 
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
      # self.prev_hop['id'] = prev_hop # Save this for dupe
      # self.next_hops = self.neighbor_list # next hop = physical neig, dictionary
      sequence_num = disco_msg[0] # should not be a single variable
      # see if these variables match a previous message within dupe
      # otherwise don't flood
      for n in self.neighbor_list:
        if n.DHT_ID == prev_hop :
          # don't flood source with same message
          continue
        else :
          print "Node ", self.DHT_ID, " flooding: ", n.DHT_ID
          n.process_message(disco_msg, self.DHT_ID)

  def who_am_i(self):
    return self.DHT_ID

  def set_neighbors(self, neigh_list):
    self.neighbor_list = neigh_list

####################################
# Will Run Main
####################################
if __name__ == '__main__':
  main()
