'''
Created on Oct 19, 2014

@author: adrian
'''
import math
import numpy as np


def main():
    points = np.array([[50, 18], [53, 10], [58, 13], [56, 13]])
    a = np.array([0,0])
    b = np.array([100, 40])
    L1 = []
    L2 = []
    
    for i in range(len(points)):
        L1a = abs(sum(points[i] - a))
        L1b = abs(sum(points[i] - b))
        L2a = math.sqrt(sum((points[i] - a)**2))
        L2b = math.sqrt(sum((points[i] - b)**2))
        L1.append([L1a, L1b])
        L2.append([L2a, L2b])
     
    L1 = np.array(L1)
    L2 = np.array(L2)
        
    print L1
    print L2   
    
    for i in range(len(L1)):
        print points[i], L1[i], L2[i]
        if (L1[i,0] - L1[i,1]) * (L2[i,0]-L2[i,1]) < 0:
            print 'Found : ', points[i]


if __name__ == '__main__':
    main()