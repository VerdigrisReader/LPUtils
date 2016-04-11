#!usr/bin/python
import sys
sys.path.append('/home/pi/python/launchpad')
from launchpad import Launchpad


class LaunchPadHandler():
    """
    
    
    """

    def __init__(self, 
                 offset = (0, 1), 
                 record_state = False, 
                 cyclic = False,
                 colorscheme=0):
        """
        Stores all of the required vars to send signals to the launchpad
        Offset arg refers to x, y offset
        Color scale runs from 0-14 (fewer options, but acts as a simple spectrum)
        
        methods include a runner, which accepts a function to act on the object
        
        """
        self.lp = Launchpad()
        self.lp.Open()
        self.lp.LedCtrlXY(0,0,0,3)
        self.lp.LedCtrlXY(0,0,0,0)
        self.offset = offset
        cols = ([(0,3),(1,3),(1,2),(2,2),(2,1),(3,1),(3,0)],
                [(3,0),(3,1),(2,1),(2,1),(2,0),(1,0),(0,0)])
        tmp = cols[colorscheme]
        if cyclic == True:
            self.colorscale = {x: y for x, y  in enumerate(tmp[:-1] + tmp[::-1][:-1])}
        else:
            self.colorscale = {x: y for x, y  in enumerate(tmp)}
        self.lp.Reset()
        self.record_state = record_state
        self.lp.state = {x: {y: -1 for y in xrange(8)} for x in xrange(8)}

    def __del__(self):
        """
        On garbage collection, reset lights
        """
        self.lp.Reset()
#        raise SystemExit
    
    def _coords(self, x, y):
        return x + self.offset[0], y + self.offset[1]
    
    def _colors(self, c):
        """
        Handles color scale. returns a color for all values
        except -1, which is equivalent to off (0, 0)
        """
        if c == -1:
            return (0, 0)
        else:
            return self.colorscale[c % len(self.colorscale)]
    
    def send(self, x, y, c = 0):
        """
        Send co-ords to launchpad, records state if necessary
        """
        x1, y1 = self._coords(x, y)
        c2, c1 = self._colors(c)
        self.lp.LedCtrlXY(x1, y1, c1, c2)
        if self.record_state:
            self[x][y] = [c]
    
    def recieve(self):
        state = self.lp.ButtonStateXY()
        if state:
            state[0] -= self.offset[0]
            state[1] -= self.offset[1]
            return state
        else:
            return None

    def _run_loop(self,func):
        while True:
            func(self)

    def run(self, func, loop = False):
        """
        Takes function as argument - function should take handler as argument
        """
        try:
            if loop:
                self._run_loop(func)
            else:
                func(self)
        except (KeyboardInterrupt, SystemExit):
            self.lp.Reset()
            raise SystemExit
        except:
            self.lp.Reset()
    
    def get_state(self,x=None,y=None):
        if x and y:
            return self.state[x][y]
        else:
            return self.state


def get_line(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
    
    stolen from online to make life easier
 
    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points
