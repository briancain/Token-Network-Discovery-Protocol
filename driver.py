import node, time, sys

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
  print "CIS 598: Senior Project\nDemo Programmed by: Brian Cain"
  print "###############################\n\n"

  x, y1, y2, z = init_Node() # Get node objects
  inter_nodes = [y1, y2]

  print "\n"
  print "Source Node ID: ", x.who_am_i()
  print "Source Node Neighbor List: ",
  for ids in x.neighbor_list :
    print ids.msg_DHT_ID,

  print "\n\nIntermediate Node ID: ", y1.who_am_i()
  print "o----------> Destination: ", y1.request_id
  print "\nIntermediate Node ID: ", y2.who_am_i()
  print "o----------> Destination: ", y2.request_id
  print "\nDestination Node ID: ", z.who_am_i()
  print "\n"


  go = mem_inv_auth() # membership invitation authority says when it can flood
  if go == True :
    string = "Flooding network..........\n\n"
    dot_load(string)
    for x1 in x.neighbor_list :
      flag = x.flood(x1)
      if not flag :
        que = x1.flood(x1.neighbor_list)

#######################################
# Initalize nodes
#######################################
def init_Node() :
  string =  "Initializing nodes....\n"
  dot_load(string)
  load()
  x = node.node_Source(1)
  load()
  y1 = node.node_Int(3, 11, x.msg_DHT_ID) # request ID and source ID
  load()
  y2 = node.node_Int(5, 11, x.msg_DHT_ID)
  load()
  z = node.node_Dest(11)
  x.neighbor_list = [y1, y2]
  y1.neighbor_list = z
  y2.neighbor_list = z

  return x, y1, y2, z

##############################################################################
# Gives the illusion that things are loading for presentation 2! ;)
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
