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
  # enable logging of processes
  multiprocessing.log_to_stderr()
  logger = multiprocessing.get_logger()
  logger.setLevel(logging.INFO)
  special_source_node_bad_design = None

  for i in range(15):
    nid = i+1
    print "[Main] Initializing Node:", nid
    queue_to = Queue() # incoming messages from Node
    queue_from = Queue() # outgoing messages from Node
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
      jobs[j][1].put(pass_list)


  # print "[DRIVER] All of the job states before flooding:", jobs
  if mem_inv_auth(): # membership invitation authority says when it can flood
    print "Flooding network.........."
    jobs[1][1].put("FLOOD")

  while True:
    for j in jobs.values():
      q = j[2] # j[2] is from queue
      try: msg = q.get_nowait() #will spin CPU, need something blocking (later)
      except: continue
      if msg[0] == "CONSTRUCT":
        # "CONSTRUCT", destination id, source id, queue
        dst_id = msg[1]
        src_id = msg[2]
        que = msg[3]
        msg_send = [msg[0], src_id, que]
        jobs[dst_id][1].put(msg_send)
      else: # flooding
        dst_id, src_id, payload = msg
        msg_send = [payload, src_id]
        jobs[dst_id][1].put(msg_send) # j[1] is to queue


  #we never expect to get here
  for p in jobs.values(): p[3].join()


###########################################
# Initialize Neighbor depending on the ID
###########################################
def init_neighbors(node_id, j):

  """
    - Neighbor List
    
  # 1: [10, 11, 15, 2]
  # 2: [1, 15, 14, 3]
  # 3: [2, 14, 5, 4]
  # 4: [3, 14, 15, 6]
  # 5: [14, 3, 4, 6]
  # 6: [4, 5, 13, 7]
  # 7: [6, 13, 8, 12]
  # 8: [7, 13, 12, 9]
  # 9: [10, 11, 12, 8]
  # 10: [1, 11, 9, 15]
  # 11: [1, 12, 9, 10]
  # 12: [11, 15, 14, 7, 9, 8]
  # 13: [14, 6, 7, 8]
  # 14: [2, 3, 4, 5, 13, 12, 15]
  # 15: [1, 2, 14, 12, 10]
  """

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
