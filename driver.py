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
  print "CIS 598: Senior Project\nProgrammed by: Brian Cain"
  print "###############################\n\n"

  x_list, y_list, z_list = init_Node() # Get node objects

  print "\nNodes initialized"

  print "Network topology:"
  print_network(x_list, y_list, z_list)

  go = mem_inv_auth() # membership invitation authority says when it can flood
  if go == True :
    print "Flooding network.........."

#######################################
# Initalize nodes
#######################################
def init_Node() :
  print "Initializing nodes....\n"
  x = node.node_Source(1)

  y2 = node.node_Int(2, 6)
  y3 = node.node_Int(3, 8)
  y4 = node.node_Int(4, 8)
  y5 = node.node_Int(5, 8)
  y7 = node.node_Int(7, 8)
  y9 = node.node_Int(9, 6)
  y10 = node.node_Int(10, 6) # request ID and source ID
  y11 = node.node_Int(11, 6)
  y12 = node.node_Int(12, 6)
  y13 = node.node_Int(13, 8)
  y14 = node.node_Int(14, 8)
  y15 = node.node_Int(15, 6)

  z1 = node.node_Dest(6)
  z2 = node.node_Dest(8)

  
  x.set_neighbors([y10, y11, y15, y2]) # 1: [10, 11, 15, 2]
  y2.set_neighbors([x, y15, y14, y3]) # 2: [1, 15, 14, 3]
  y3.set_neighbors([y2, y14, y5, y4]) # 3: [2, 14, 5, 4]
  y4.set_neighbors([y3, y14, y5, z1]) # 4: [3, 14, 15, 6]
  y5.set_neighbors([y14, y3, y4, z1]) # 5: [14, 3, 4, 6]
  y7.set_neighbors([z1, y13, z2, y12]) # 7: [6, 13, 8, 12]
  y9.set_neighbors([y10, y11, y12, z2]) # 9: [10, 11, 12, 8]
  y10.set_neighbors([x, y11, y9, y15]) # 10: [1, 11, 19, 15]
  y11.set_neighbors([x, y12, y9, y10]) # 11: [1, 12, 9, 10]
  y12.set_neighbors([y11, y15, y14, y7, y9, z2]) # 12: [11, 15, 14, 7, 9, 8]
  y13.set_neighbors([y14, z1, y7, z2]) # 13: [14, 6, 7, 8]
  y14.set_neighbors([y2, y3, y4, y5, y13, y12, y15]) # 14: [2, 3, 4, 5, 13, 12, 15]
  y15.set_neighbors([x, y2, y14, y12, y10]) # 15: [1, 2, 14, 12, 10]

  
  z1.set_neighbors([y4, y5, y13, y7]) # 6: [4, 5, 13, 7]
  z2.set_neighbors([y7, y13, y12, y9]) # 8: [7, 13, 12, 9]
  
  x_list = [x]
  y_list = [y2, y3, y4, y5, y7, y9, y10, y11, y12, y13, y14, y15]
  z_list = [z1, z2]
  return x_list, y_list, z_list

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

##############################################################
# Prints network topology with neighbor list
##############################################################
def print_network(x_list, y_list, z_list):
  print "\n"
  for x in x_list:
    print "Source Node ID: ", x.who_am_i()
    print "[",
    for xn in x.neighbor_list:
      print xn.who_am_i(), ",",
    print "]"
  print "\n"

  for y in y_list:
    print "Intermediate Node ID: ", y.who_am_i()
    print "[",
    for yn in y.neighbor_list:
      print yn.who_am_i(), ",",
    print "]"

  print "\n"

  for z in z_list:
    print "Source Node ID: ", z.who_am_i()
    print "[",
    for zn in z.neighbor_list:
      print zn.who_am_i(), ",",
    print "]"

  print "\n"

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
