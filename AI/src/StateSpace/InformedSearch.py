'''
Created on Jan 27, 2015

@author: adrian
'''

from Queue import PriorityQueue

class AStar:
    def __init__(self, stateClass, start, goal):
        self.path = []   #solution we are building
        self.visited = {}   # cut loops
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal
        self.startState = stateClass(self.start, 0,
                                  self.start, self.goal)        
    def Solve(self, loopCheck):
        count = 0 # incremental id for children created

        # put the initial state in the queue
        # the first value is the priority (distance to goal)
        # in this case it doesn't matter because the queue is empty 
        # and the node will be popped immediately
        self.priorityQueue.put((0, count, self.startState))
        
        # while we haven't found a path (path is empty)
        # and the there are still successor states to visit (priorityQueue is not empty)
        while(not self.path and self.priorityQueue.qsize()):
            # each PQ node stores a value that is a tuple, representing a state to be visited
            # the state is stored in the 3rd place of the tuple (zero-based [2])
            # we pop the state with min distance from the goal            
            closestChild = self.priorityQueue.get()[2]
            closestChild.createChildren()
            if loopCheck:
                self.visited[closestChild.value] = closestChild.getDistToOrigin()
            #print (closestChild.path)
            for child in closestChild.children:
                if loopCheck:
                    # the below turns the A* from a tree search into a graph search
                    # by preventing infinite loops in graphs 
                    # (note that it may loose some optimal paths
                    # if exploring more than one path to a node
                    # to there is more than one valid path to a node)
                    # that is why I use a dict instead of a set, to store the distance to origin
                    if child.value in self.visited and self.visited[child.value] <= child.getDistToOrigin():
                        continue
                    else:
                        self.visited[child.value] = child.getDistToOrigin()
                
                count += 1
                # if the distance is zero we reached the goal
                if not child.distToGoal:
                    self.path = child.path
                    break
                # in proper A*, we explore next the node with the shortest path from origin to goal
                # (not just the node closest to the goal, like in greedy best-first-search)
                # f() = g() + h() 
                self.priorityQueue.put((child.getDistToOrigin() + child.distToGoal, count, child))

            
        if not self.path:
            print("Goal of " + self.goal + " is not possible")
        print("Number of successors created: %d" % count)

        return self.path           
        
       
    def CountStatesAtDepthFromGoal(self, requiredDepth):
        count = 0 # incremental id for children created
        maxDepth = 0
        statesAtRequiredDepth = 0
        self.priorityQueue.put((0, count, self.startState))
        
        # while we haven't found a path (path is empty)
        # and the there are still successor states to visit (priorityQueue is not empty)
        while(self.priorityQueue.qsize()):
            # each PQ node stores a value that is a tuple, representing a state to be visited
            # the state is stored in the 3rd place of the tuple (zero-based [2])
            # we pop the state with min distance from the goal
            closestState = self.priorityQueue.get()         
            closestChild = closestState[2]
            
            if closestChild.value in self.visited:
                continue 

            self.visited[closestChild.value] = closestChild.depth
            
            if closestChild.depth == requiredDepth:
                statesAtRequiredDepth += 1                              
                continue  
                 
            if closestChild.getDistToOrigin() > maxDepth:
                maxDepth = closestChild.getDistToOrigin()            
                    
            closestChild.createChildren()
            for child in closestChild.children:
                # the below prevents exploring more than one path to a node
                # to cut infinite loops in graphs 
                # (note that it may loose some optimal paths)
                if child.value not in self.visited:                                          
                    count += 1
                    # the states of minimal depth are processed first,
                    # this ensure the process goes in bread-first-search order
                    self.priorityQueue.put((child.depth, count, child))
                    
        if statesAtRequiredDepth == 0:
            print("Depth of %d is not attainable" % requiredDepth)
            print("Max Depth: %d" % maxDepth)

        print("Number of successors created: %d" % count)
        print("States at depth %d: %d" % (requiredDepth, statesAtRequiredDepth))

        return statesAtRequiredDepth
            
        
