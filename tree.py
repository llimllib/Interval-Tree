import itertools

class Node(object):
    def __init__(self):
        self.xmid = None

        #the set of all intervals containing xmid, sorted by starting point
        # (l_left) and ending point (l_right)
        self.l_left = None
        self.l_right = None

        #left and right pointers
        self.ileft = None
        self.iright = None

        self.nodes = 0

def flatten(lst):
    return itertools.chain.from_iterable(lst)

def median(intervals):
    midpoint = int((len(intervals)*2)/2)
    return sorted(flatten(intervals))[midpoint]

def contains(pt, intervals):
    return [(i,j) for i,j in intervals if i <= pt <= j]

def left(pt, intervals):
    """return all intervals entirely to the left of pt"""
    return [(i,j) for i,j in intervals if j < pt]

def right(pt, intervals):
    """return all intervals entirely to the right of pt"""
    return [(i,j) for i,j in intervals if i > pt]

def maketree(intervals):
    """given a list of pairs, return the root of an interval tree. Assumes pairs are sorted.
    
    Implemented directly from Computational Geometry, de Berg et al, 3rd ed pp. 223-224"""
    if len(intervals) == 0:
        return Node()
    else:
        v = Node()
        v.xmid = median(intervals)
        v.nodes = len(intervals)

        midpairs  = contains(v.xmid, intervals)
        v.l_left  = sorted(midpairs)
        v.l_right = sorted(midpairs, key=lambda x: x[1])

        v.ileft  = maketree(left(v.xmid, intervals))
        v.iright = maketree(right(v.xmid, intervals))

        return v

def querytree(v, q):
    """given a root node v, return a list of all intervals containing q
    
    Implemented directly from Computational Geometry, de Berg et al, 3rd ed pp. 223-224"""
    if not v.nodes: return []

    if q < v.xmid:
        c = []
        for i,j in v.l_left:
            if i <= q: c.append((i,j))
            else: break
        return c + querytree(v.ileft, q)
    else:
        c = []
        for i,j in v.l_right:
            if j >= q: c.append((i,j))
            else: break
        return c + querytree(v.iright, q)

x = [(1,3), (2,2), (-1,0)]
root = maketree(x)
twos = querytree(root, 2)
