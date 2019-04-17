import sys, os
import termios, fcntl
import select
import time

fd = sys.stdin.fileno()
newattr = termios.tcgetattr(fd)

oldterm = termios.tcgetattr(fd)
oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)

newattr[3] = newattr[3] & ~termios.ICANON
newattr[3] = newattr[3] & ~termios.ECHO

fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

termios.tcsetattr(fd, termios.TCSANOW, newattr)

def getch_glenn():
  try:
    return sys.stdin.read()
  except (IOError, TypeError) as e:
    return None

print "Type some stuff"
while True:
  key = getch_glenn()
  if key == 'q':
     break    
  if key:
    print("-%s" % key)
  else:
    print("None")

  time.sleep(.2)

# Reset the terminal:
termios.tcsetattr(fd, termios.TCSANOW, oldterm)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
