#!usr/bin/python
import random
import itertools
import time
from lputils import get_line
from copy import copy
import math

def pattern1(lp):
    
    i = 0
    ords = sorted(itertools.product(range(8),range(8)))
    groups = {}
    for o in ords:
        s = sum(o)
        if s in groups:
            groups[s].append(o)
        else:
            groups[s] = [o]
    brn = 0
    while brn < 200:
        brn += 1
        for key in sorted(groups.keys()):
            for x, y in groups[key]:
                lp.send(x,y,key + i)
            n = lp.recieve()
            if n:
                i = n[0] + n[1]
            time.sleep(0.01)
        i = (i +  1) % 18


def pattern2(lp):
    origin = (4, 4)
    ords = sorted(itertools.product(range(8),range(8)))
    def calc_groups(origin, ords):
        groups = {}
        lx = lambda x,y : (sum([(a-b)**2 for a, b in zip(*(x,y))])**0.5)*2
        for ord in ords:
            n = int(lx(ord,origin))
            if n in groups:
                groups[n].append(ord)
            else:
                groups[n] = [ord]
        return groups
    groups = calc_groups(origin, ords)
    i = 0
    while i < 400:
        for key in sorted(groups.keys()):
            for x, y in groups[key]:
                lp.send(x,y,key + i)
            time.sleep(0.03)
            n = lp.recieve()
            if n:
                print n
                origin = (n[0], n[1])
                groups = calc_groups(origin, ords)
                i = 0
        i += 1



def pattern3(lp):
    def calc_groups(origin, ords):
        lx = lambda x, y: sum([abs((a-b))**1.5 for a, b in zip(*(x,y))])**0.6666
#        lx = lambda x, y: sum([abs((a-b))**2 for a, b in zip(*(x,y))])**0.5

        groups = [(int(lx(origin, ord)), ord[0], ord[1]) for ord in ords]
        return sorted(groups,key=lambda x: x[0])
    def run1(lp,groups,val, n):
        for r1 in xrange(n):
            sel1 = [(y,z) for x,y,z in groups if x == val - r1]
            if r1 != n - 1:
                for x,y in sel1:
                    lp.send(x,y,val+r1)
            else:
                for x,y in sel1:
                    lp.send(x,y,-1)
        time.sleep(0.03)
    def run_for_origin(lp, origin):
        groups = calc_groups(origin,list(itertools.product(range(8),range(8))))
        tmp = zip(*groups)[0]
        for n in range(min(tmp),max(tmp)+3):
            run1(lp,groups,n,3)
    l = list(itertools.product(range(8),range(8)))
    for brn in xrange(70):
        r = lp.recieve()
        if r:
            new = lp.recieve()
            while new:
                r = new
                new = lp.recieve()
            origin = (r[0], r[1])
        else:
            origin = random.choice(l)
        run_for_origin(lp, origin)
        time.sleep(random.random()/3.0)
        r = None


def pattern4(lp):
    ords = list(itertools.product(*[range(8)]*2))
    state = {}
    for x in ords:
        state[x] = random.choice([2,3,1,7,8,9])
    deltas = [x for x in itertools.product(*[range(-1,2)]*2)]
    for step in xrange(900):
#        r = lp.recieve()
#        if r:
#            while new:
#                r = new
#                new = lp.recieve()
#            adbrs = [(x+r[0],y+r[1]) for x,y in deltas +[(0,0)] ]
#            for xy in adbrs:
#                try:
#                    state[xy] += 2
#                    lp.send(xy[0],xy[1],state[xy])
#                except:
#                    pass
            
    
        pnt = random.choice(ords)
        pntval = state[pnt]
        adjs = [(x+pnt[0],y+pnt[1]) for x,y in deltas]
        comps = filter(lambda x: x is not None,[state.get(b) for b in adjs])
        ave = float(sum(comps))/float(len(comps))
        if ave > pntval:
            state[pnt] -= 1
        elif ave < pntval:
            state[pnt] += 1
        else:
            state[pnt] += random.choice([-3,-2,3,2])
        lp.send(pnt[0],pnt[1],state[pnt])
        time.sleep(0.02)


def pattern5(lp):
    points = []
    k = -0.00052
    for x in xrange(9):
        points.append({'prev':(1,1),'cntr':(random.randint(0,8),
                       random.randint(0,8)),
                       'col':0,'x':random.random()*8,'y':random.random()*8,
                       'dx':random.random()/9,'dy':random.random()/9})
    for x in xrange(len(points)):
        another = range(len(points))
        another.remove(x)
        points[x]['in'] = random.choice(another)
    for step in xrange(400):
        for pnt in points:
            ip =  points[pnt['in']]
            cx = (ip['x'] + 4) / 2.0
            cy = (ip['y'] + 4) / 2.0
# 
#            print pnt['x'], pnt['y'], pnt['dx'], pnt['dy']
            pnt['x'] += float(pnt['dx'])
            pnt['y'] += float(pnt['dy'])
            lp.send(int(pnt['x']),int(pnt['y']),pnt['col'])
            pnt['col'] = pnt['col'] + 1
            pnt['dx'] += k * (pnt['x'] - cx)
            pnt['dy'] += k * (pnt['y'] - cy)
            if int(pnt['x']) != pnt['prev'][0] or int(pnt['y']) != pnt['prev'][1] :
                lp.send(pnt['prev'][0],pnt['prev'][1],-1) 
                pnt['prev'] = (int(pnt['x']), int(pnt['y']))
        time.sleep(0.01)



def rotation(lp):
    corners = [(0,0),(0,7),(7,7),(7,0)]
    path = reduce(lambda x,y: x + y,[get_line(a,b) for a,b in zip(corners, corners[1:] + corners[:1])])
    remove_adj = lambda nums : [a for a,b in zip(nums, nums[1:]+[not nums[-1]]) if a != b]
    path = remove_adj(path)
    locs = (itertools.cycle(path[:-1]), itertools.cycle(path[len(path)/2:-1] + path[:len(path)/2]))
    base = 0
    baseadd = random.choice((0.8,1,1.5,2,2.8,3.7))
    slowfast = False
    for step in xrange(900):
        p1, p2 = (x.next() for x in locs)
        i = 0
        for x, y in get_line(p1,p2):
            lp.send(x,y,math.floor(base)+i)

            i += 1
        base += baseadd
        r = random.random()
        if lp.recieve():
            print 'change'
            slowfast = not slowfast
        elif r < 0.005:
            slowfast = not slowfast
        if slowfast:
            time.sleep(0.03)
        else:
            time.sleep(0.008)










patterns = [pattern1, 
            pattern2, 
            pattern3, 
            pattern4, 
            pattern5, 
            rotation]
