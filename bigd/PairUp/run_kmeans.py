# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 18:00:49 2016

@author: adrian
"""

import KMeans as km
import random


inputs = [[-0.5, 0.6], [0.1, 0.0], [3.0, 2.0], [-0.4, 0.2], [3.4, 4.0], [2.9, 3.0], [6.9, 7.0], [8.0, 6.5], [7.5, 6.8], [0.4, -0.6], [3.3, 2.6]]
if __name__ == '__main__':

    random.seed(0)
    algo = km.KMeans(3)
    algo.train(inputs)
    print "K-Means completed successfully: "
    for i in range(len(algo.means)):
        print "%d: (%.2f, %.2f)" % (i, algo.means[i][0], algo.means[i][1] )
        
    
    
    