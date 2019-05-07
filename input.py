###############################
#  Imports for reading keyboard
##############################
import sys, os
import termios, fcntl

# Time is used in our main loop for delay functionality.
import time

################################
#  Initialize keyboard reading. 
#  Save the old terminal configuration, and
#  tweak the terminal so that it doesn't echo, and doesn't block.
################################
fd = sys.stdin.fileno()
newattr = termios.tcgetattr(fd)

oldterm = termios.tcgetattr(fd)
oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)

newattr[3] = newattr[3] & ~termios.ICANON
newattr[3] = newattr[3] & ~termios.ECHO

fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

termios.tcsetattr(fd, termios.TCSANOW, newattr)

##################################
# Non-blocking character read function.
#################################
def getch_noblock():
  try:
    return sys.stdin.read()
  except (IOError, TypeError) as e:
    return None

print "Type some stuff"
while True:
  key = getch_noblock()
  if key == 'q':
     break    
  if key:
    print("-%s" % key)
  else:
    print("None")

  time.sleep(.2)

###################################
# Reset the terminal on exit
###################################
termios.tcsetattr(fd, termios.TCSANOW, oldterm)

fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
