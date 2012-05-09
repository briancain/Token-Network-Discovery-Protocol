import node, time, sys, multiprocessing, logging
from multiprocessing import Process, Queue

###############################################################

#   CIS 598 Senior Project by Brian Cain

#   bccain@ksu.edu

#   driver.py - runs code

###############################################################


#######################################
# Main Driver Code
#######################################

def main() :
  print "###############################"
  print "CIS 598: Senior Project\nProgrammed by: Brian Cain"
  print "###############################\n\n"


  jobs = dict()
  multiprocessing.log_to_stderr()
  logger = multiprocessing.get_logger()
  logger.setLevel(logging.INFO)
  special_source_node_bad_design = None

  for i in range(15):
    nid = i+1
    print "Main: Initializing Node:", nid
    queue_to = Queue()
    queue_from = Queue()
    x = node.node(nid)
    if nid is 1:
      special_source_node_bad_design = x

    p = Process(target=x.run_node, args=(i,queue_to,queue_from))
    jobs[nid] = (x, queue_to, queue_from, p) #Node (x) is first element (NOT p)
    p.start()
    while not p.is_alive(): time.sleep(0.1) #make sure it's constructed

	#print "Driver initialized node", x, "with Queues", queue_from, queue_to

  for j in jobs:
    lst = init_neighbors(j, jobs)
    pass_list = ["LIST",  lst]
    if lst is None:
      print "List is null, failure"
      exit()
    else:
      # jobs[j][0].set_neighbors(lst) # this will fail, pass list through Queue
      jobs[j][1].put(pass_list)


  # print "[DRIVER] All of the job states before flooding:", jobs
  if mem_inv_auth(): # membership invitation authority says when it can flood
    print "Flooding network.........."
    # time.sleep(3)
    jobs[1][1].put("FLOOD")

  while True:
    for j in jobs.values():
      q = j[2] # j[2] is from queue
      try: msg = q.get_nowait() #will spin CPU, need something blocking (later)
      except: continue
      if msg[0] == "CONSTRUCT":
        print "\n\n\n\n\n\n\n\nCONSTRUCT THE TOKENS"
        # "CONSTRUCT", destination id, source id, queue
        dst_id = msg[1]
        src_id = msg[2]
        que = msg[3]
        msg_send = [msg[0], src_id, que]
        jobs[dst_id][1].put(msg_send)
      else:
        dst_id, src_id, payload = msg
        msg_send = [payload, src_id]
        jobs[dst_id][1].put(msg_send) # j[1] is to queue


  #we never expect to get here
  for p in jobs.values(): p[3].join()


###########################################
# Initialize Neighbor depending on the ID
###########################################
def init_neighbors(node_id, j):

  if node_id == 1:
    list_neigh = [j[10][0], j[11][0], j[15][0], j[2][0]]
  elif node_id == 2:
    list_neigh = [j[1][0], j[15][0], j[14][0], j[3][0]]
  elif node_id == 3:
    list_neigh = [j[2][0], j[14][0], j[5][0], j[4][0]]
  elif node_id == 4:
    list_neigh = [j[3][0], j[14][0], j[5][0], j[6][0]]
  elif node_id == 5:
    list_neigh = [j[14][0], j[3][0], j[4][0], j[6][0]]
  elif node_id == 6:
    list_neigh = [j[4][0], j[5][0], j[13][0], j[7][0]]
  elif node_id == 7:
    list_neigh = [j[6][0], j[13][0], j[8][0], j[12][0]]
  elif node_id == 8:
    list_neigh = [j[7][0], j[13][0], j[12][0], j[9][0]]
  elif node_id == 9:
    list_neigh = [j[10][0], j[11][0], j[12][0], j[8][0]]
  elif node_id == 10:
    list_neigh = [j[1][0], j[11][0], j[9][0], j[15][0]]
  elif node_id == 11:
    list_neigh = [j[1][0], j[12][0], j[9][0], j[10][0]]
  elif node_id == 12:
    list_neigh = [j[11][0], j[15][0], j[14][0], j[7][0], j[9][0], j[8][0]]
  elif node_id == 13:
    list_neigh = [j[14][0], j[6][0], j[7][0], j[8][0]]
  elif node_id == 14:
    list_neigh = [j[2][0], j[3][0], j[4][0], j[5][0], j[13][0], j[12][0], j[15][0]]
  elif node_id == 15:
    list_neigh = [j[1][0], j[2][0], j[14][0], j[12][0], j[10][0]]
  else :
    print "Invalid Node ID"
    return None

  return list_neigh

#######################################
# Initalize nodes
#######################################
def init_Node() :
  print "Initializing nodes....\n"
  x = node.node(1)

  x2 = node.node(2)
  x3 = node.node(3)
  x4 = node.node(4)
  x5 = node.node(5)
  x6 = node.node(6)
  x7 = node.node(7)
  x8 = node.node(8)
  x9 = node.node(9)
  x10 = node.node(10) 
  x11 = node.node(11)
  x12 = node.node(12)
  x13 = node.node(13)
  x14 = node.node(14)
  x15 = node.node(15)

  x.set_neighbors([x10, x11, x15, x2]) # 1: [10, 11, 15, 2]
  x2.set_neighbors([x, x15, x14, x3]) # 2: [1, 15, 14, 3]
  x3.set_neighbors([x2, x14, x5, x4]) # 3: [2, 14, 5, 4]
  x4.set_neighbors([x3, x14, x5, x6]) # 4: [3, 14, 15, 6]
  x5.set_neighbors([x14, x3, x4, x6]) # 5: [14, 3, 4, 6]
  x6.set_neighbors([x4, x5, x13, x7]) # 6: [4, 5, 13, 7]
  x7.set_neighbors([x6, x13, x8, x12]) # 7: [6, 13, 8, 12]
  x8.set_neighbors([x7, x13, x12, x9]) # 8: [7, 13, 12, 9]
  x9.set_neighbors([x10, x11, x12, x8]) # 9: [10, 11, 12, 8]
  x10.set_neighbors([x, x11, x9, x15]) # 10: [1, 11, 9, 15]
  x11.set_neighbors([x, x12, x9, x10]) # 11: [1, 12, 9, 10]
  x12.set_neighbors([x11, x15, x14, x7, x9, x8]) # 12: [11, 15, 14, 7, 9, 8]
  x13.set_neighbors([x14, x6, x7, x8]) # 13: [14, 6, 7, 8]
  x14.set_neighbors([x2, x3, x4, x5, x13, x12, x15]) # 14: [2, 3, 4, 5, 13, 12, 15]
  x15.set_neighbors([x, x2, x14, x12, x10]) # 15: [1, 2, 14, 12, 10]

  x_list = [x, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15]
  print "\nNodes initialized"
  return x_list

##############################################################################
# Gives the illusion that things are loading for presentation 2! ;)
# Might be used later for when stuff takes a while to load
# Code referenced : http://www.stealth-x.com/articles/python-code-tricks.php
##############################################################################
def dot_load(ch):
  for character in ch:
	sys.stdout.write(character)
	sys.stdout.flush()
	time.sleep(.03)

def load():
  sys.stdout.write("o Loading....  ")
  sys.stdout.flush()
  round = 0
  type = 0
  while round != 12:
    if type == 0: sys.stdout.write("\b/")
    if type == 1: sys.stdout.write("\b-")
    if type == 2: sys.stdout.write("\b\\")
    if type == 3: sys.stdout.write("\b|")
    type += 1
    round += 1
    if type == 4: type = 0
    sys.stdout.flush()
    time.sleep(0.2)
  print "\b\b done!"

###################################################
# Membership and Invitation Authority will say
# when node can flood
###################################################
def mem_inv_auth() :
  return True

#########################################################
# Runs main
#########################################################
if __name__ == '__main__':
  main()
