#!usr/bin/python
import sys
import random
import time
import itertools

from lputils import LaunchPadHandler
from patterns import patterns


if __name__ == "__main__":

    lp = LaunchPadHandler(cyclic=False,
                          colorscheme=0)
    
    if sys.argv[1:]:
        lp.run(patterns[int(sys.argv[1])])
    else:    
        lp.run(patterns[0])
    
    if sys.argv[2:]:
        while True:
            pt = random.choice(patterns)
            print pt
            lp.run(pt)
            lp.lp.Reset()
