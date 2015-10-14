'''
Created on Oct 21, 2014

@author: adrian
'''

import numpy as np
from numpy.linalg import norm



def find_orthogonal(u, candidates):
    for i in range(len(candidates[:, 0])):
        print 'row nr %d: %s  . %s = %f  - norm(%s) = %f' % (i, candidates[i,:], u, np.dot(candidates[i,:], u), candidates[i,:], norm(candidates[i,:]))


def main():
    # Q01 Singular Value decomposition    
    u = np.array([2.0/7, 3.0/7, 6.0/7])   
    candidates = np.array([[2.250, -.500, -.750], [.728, .485, -.485], [-.286, -.429, .857], [1.125, .500, -.625]])
    find_orthogonal(u, candidates)


if __name__ == '__main__':
    main()