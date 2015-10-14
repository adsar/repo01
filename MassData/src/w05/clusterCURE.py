'''
Created on Nov 11, 2014

@author: adrian
'''

from matplotlib.mlab import dist
import numpy as np


def min_dist(point, ps, k):
    mind = 0
    first = True
    for j in ps.keys():
        if dist(point[k], ps[j]) < mind or first:
            mind = dist(point[k], ps[j])
            first = False
    return mind


def assign_CURE(point, ps, count):
    for i in range(1, count):
        maxd = 0
        maxp = ''
        first = True
        for k in point.keys():
            if k not in ps:
                d = min_dist(point, ps, k)
                if d > maxd or first:
                    maxd = d
                    maxp = k
                    first = False
        
        print "point %d: %s  at min dist = %d" % (i, maxp, maxd)
        ps[maxp] = point[maxp]

def main():
    point = {}
    point['x'] = np.array([0,0])
    point['y'] = np.array([10,10])
    point['a'] = np.array([1,6])
    point['b'] = np.array([3,7])
    point['c'] = np.array([4,3])
    point['d'] = np.array([7,7])
    point['e'] = np.array([8,2])
    point['f'] = np.array([9,5])
    
    print point
    
    print dist(point['x'], point['y'])
    

    ps = {}
    ps['x'] = point['x']
    ps['y'] = point['y']
    
    assign_CURE(point, ps, 6)        

    print ps



if __name__ == '__main__':
    main()