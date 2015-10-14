#usr/bin/env python

'''
Created on Jan 28, 2015

@author: adrian
'''

import StateSpace.InformedSearch as infs
import StateSpace.States as st


def main():
    print("Word Distance")
    start1 = "abcdefghi"
    goal1 = "gihbadfec"
    print ("starting ...")
    aStar = infs.AStar(st.State_String, start1, goal1)
    aStar.Solve(False)
    for i in xrange(len(aStar.path)):
        print ("%d) " %i + aStar.path[i]) 
    
        
    print
    print("Q1 - Eight-Puzzle - (loop check)")
    start1 = "164870325"
    goal1 = "012345678"
    print ("starting ...")
    aStar = infs.AStar(st.State_NPuzzle, start1, goal1)
    aStar.Solve(True)
    for i in xrange(len(aStar.path)):
        print ("%d) " %i + aStar.path[i]) 
    
    print
    print("Q2 - Eight-Puzzle - (loop check)")
    start2 = "817456203"
    goal2 = "012345678"
    print ("starting ...")
    aStar = infs.AStar(st.State_NPuzzle, start2, goal2)
    aStar.Solve(True)
    for i in xrange(len(aStar.path)):
        print ("%d) " %i + aStar.path[i]) 
    
    '''
    print
    print("Fifteen-Puzzle- (loop check)")
    start3 = "9C85AEBF02476D31"
    goal3 = "0123456789ABCDEF"
    print ("starting ...")
    aStar = StateSpace.InformedSearch(st.State_NPuzzle, start3, goal3)
    aStar.Solve(True)
    for i in xrange(len(aStar.path)):
        print ("%d) " %i + aStar.path[i]) 
        '''

    print
    print("Q3 - Eight-Puzzle - (loop check) - states at depth 27")
    start3 = "012345678"
    goal3 = "012345678"
    print ("starting ...")
    aStar = infs.AStar(st.State_NPuzzle, start3, goal3)
    aStar.CountStatesAtDepthFromGoal(27)
    for i in xrange(len(aStar.path)):
        print ("%d) " %i + aStar.path[i]) 
            
if __name__ == '__main__':
    main()