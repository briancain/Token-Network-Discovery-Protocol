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
  print "We're in main!\n\n"
  print "##########################"
  print "CIS 598: Senior Project\nDemo Programmed by: Brian Cain"
  print "##########################\n\n"

  x, y, z = init_Node() # Get node objects

  print "\n"
  print "Source Node ID: ", x.who_am_i()
  print "Intermediate Node ID: ", y.who_am_i()
  print "Destination Node ID: ", z.who_am_i()
  print "\n"


  go = mem_inv_auth() # membership invitation authority says when it can flood
  if go == True :
    x.flood()

def init_Node() :
  print "Initializing nodes:"
  char = "............................"
  dot_load(char)
  print "\n"
  load()
  x = node.node_Source()
  load()
  y = node.node_Int(11, x.msg_DHT_ID) # request ID and source ID
  load()
  z = node.node_Dest(4, "pref", None, 2)
  return x, y, z

##############################################################################
# Gives the illusion that things are loading for presentation
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
