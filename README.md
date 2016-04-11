# LPUtils
Simple wrapper for interacting with Novation Launchpad, built on top of FMMT666's launchpad.py

Requirements:
https://github.com/FMMT666/launchpad.py

## lputils.py
Contains the LaunchPadHandler class, which can be initialised with a few arguments, allowing for
This allows
Main methods are:
send(self,x, y, c = 0)
Sends an LED change command to a co-ordinate on the Launchpad. x, y are co-ordinates, while c is an integer refering to a location in a 'colorscale' which is passed to the instance (work in progress). c = -1 turns an LED off.
recieve(self)
Returns [(x, y, state)] for the next buttonpress in the queue.
run(self,func,loop=False)
Takes a function as an argument. The function must take only a launchpad handler as an argument.
get_state(x,y)
If record_state is True, this will retrieve the currnet state of the given button

Note:
As this library was written on a raspberry pi, the first lines of lputils.py appends the location of the home directory of the underlying launchpad.py library.


## patterns.py
Contains functions that can be passed to the LaunchPadHandler.run() method.
Current usage is import patterns from patterns.

## run.py
Command line utility which instantiates a LaunchPadHandler, imports patterns and passes pattern functions to the handler's run() method. 
Currently accepts two args. First arg is the index of the pattern to be run. If a second arg is present, the script will continue to run randomly selected patterns ad inf. Soon to be implemented as an argparser



## Example Usage:

from lputils import LaunchPadHandler
from patterns import patterns
lp = LaunchPadHandler()
lp.run(patterns[0])


## To do:
implement colorscale as a class rather a than messy list of tuples
.recievelatest() method: gets most recently pressed button, rather than next in the queu
.run() should handle args & kwargs
lphandler should store a better representation of its own state
define better object to be passed to a new '.run()' command, which sets up and stores its own attributes, and takes a simple function to generate the next state. Would allow for a more structured version of what is currently done by functions in patterns.py
