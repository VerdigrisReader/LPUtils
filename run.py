#!usr/bin/python
import random
import argparse
from datetime import datetime, datediff

from lputils import LaunchPadHandler
from patterns import patterns


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Run Launchpad Patterns')
    parser.add_argument("i",type=int)
    parser.add_argument("--loop", action="store_true")
    parser.add_argument("--green",action="store_true")
    parser.add_argument("--cyclic",action="store_true")   
    
    print parser
    
    pattern_choice, loop, green, cyclic = parser.parse_args()
    
    if green:
        lp = LaunchPadHandler(cyclic=cyclic,
                              colorscheme=1)
    else:
        lp = LaunchPadHandler(cyclic=cyclic,
                              colorscheme=0)
    
    if not loop:
        lp.run(patterns[pattern_choice])
    else:
        endtime = datetime.now() + datediff(minutes=12)
        while datetime.now() < endtime:
            pt = random.choice(patterns)
            print pt
            lp.run(pt)
            lp.lp.Reset()
