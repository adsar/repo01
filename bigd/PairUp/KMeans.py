# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 17:52:25 2016

@author: adrian
"""
import random
import util as ut
    
class KMeans:
    """performs k-means clustering"""
    
    def __init__(self, k):
        self.k = k
        self.means = None
        
    def classify(self, item):
        """takes as input one single point (item) and computes the distances to the 
        item from each of the k means (cluster centers), then chooses the min() to 
        return the index of the cluster closest to the item (point)"""
        return min(range(self.k),
                   key=lambda i: ut.squared_distance(item, self.means[i]))

    def train(self, items):
        #choose k elements at random from the data items (points) as the initial means
        self.means = random.sample(items, self.k)
        
        """ assignments is an integer array of the same length as the
            item (points) array, each element in assignments is an index
            into the array of means (cluster centers), so these are 
            integers in the range [0,k-1]"""
        assignments = None
        
        while True:
            # Find new assignments
            new_assignments = map(self.classify, items)
            
            # if no assignments have changed, we're done
            if assignments == new_assignments:
                return
            
            #otherwise keep the new assignments
            assignments = new_assignments
            
            # and compute the menas based on the new assign,ents
            for i in range(self.k):
                """find all the items (points) p assignend to cluster i 
                (where i and a are indexes to the means array, with values in [0,k-1])
                The zip-ed arrays items and assignments are enumerated together, with 
                one element from items going to p and one from assignments going to a"""
                i_points = [p for p, a in zip(items, assignments) if a == i]
                
                # make sure i_points is not empty so we don't didvide by zero
                if i_points:
                    self.means[i] = ut.vector_mean(i_points)
        
        