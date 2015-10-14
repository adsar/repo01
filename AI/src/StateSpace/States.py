
'''
Created on Jan 27, 2015

@author: adrian
'''
import numpy as np

class State(object):
    '''
    Base class for aStar states algorithms
    '''

    def __init__(self, value, parent,
                 start = 0, goal = 0):
        '''
        Children states are created with a value and a parent.
        The defaults are for the first start state,
        after that all the children will be able to
        copy the start and goal states from the parent.
        '''
        self.children = []
        self.parent = parent
        self.value = value
        self.distToGoal = 0   # place-holder, will be set in the subclasses
        self.depth = 0  # set based on parent node
        
        if parent:
            self.path = parent.path[:] #deep copy
            self.path.append(value)
            self.start = parent.start
            self.goal = parent.goal
            self.depth = parent.depth + 1
        else:
            self.path = [value]
            self.start = start
            self.goal = goal
            
    # aka g()
    def getDistToOrigin(self):
        pass 
    # aka h()      
    def getDistToGoal(self):
        pass
    '''
    Creates successor states by exploring all the 
    possible actions allowed by the constrainsts of the problem
    '''    
    def createChildren(self):
        pass
    
class State_String(State):
    def __init__(self, value, parent, 
                 start = 0, goal = 0):
        super(State_String, self).__init__(value, parent, 
                            start, goal)

        self.distToGoal = self.getDistToGoal()
        
    def getDistToOrigin(self):
        return 0 # implement greedy Best-First-AIPlanLib (not really A*)
   
    def getDistToGoal(self):
        if self.value == self.goal:
            return 0
        dist = 0
        for i in range(len(self.goal)):
            letter = self.goal[i]
            # distance from letter from its target placement
            dist += abs(i - self.value.index(letter)) 
        return dist
    
    def createChildren(self):
        if not self.children:
            # generate all possible arrangements of letters
            # xrange is range of indexes [0, N-1], in this case it will be [0, len(goal)-2]
            for i in xrange(len(self.goal)-1):
                val = self.value
                #switch the 1st and 2nd letter of every pair of letters
                val = val[:i] + val[i+1] + val[i] + val[i+2:]
                child = State_String(val, self)
                self.children.append(child)
   
class State_NPuzzle(State):
    def __init__(self, value, parent, 
                 start = 0, goal = 0):
        super(State_NPuzzle, self).__init__(value, parent, 
                                           start, goal)
        self.puzzleSize = int(np.sqrt(len(self.goal)))
        self.distToGoal = self.getDistToGoal()

    

    def nummeric(self, string):
        nr = 0
        if '0' <= string and string <= '9':
            nr = int(string)
        else:
            nr = 10 + (ord(string) - ord('A'))
        return nr

    # also known as function g()
    # if we return zero, then we turn A* into greedy BFS
    def getDistToOrigin(self):
        return self.depth

    # also known as heuristic function h()
    def getDistToGoal(self):
        if self.value == self.goal:
            return 0
        
        # calculate the Manhattan distance in the grid
        dist = 0
        n = self.puzzleSize 
        for i in range(len(self.value)):           
            # calc the coords of where the tile currently in this cell should be
            tile = self.value[i]
            t = self.nummeric(tile)    
            tile_goal_coordinates = np.array([t // n, t % n])
            
            # calc the coords of the cell where it actually is
            cell_coordinates = np.array([i // n, i % n])          
            
            d = abs(tile_goal_coordinates - cell_coordinates)            
            dist += d[0] + d[1]
            
        return dist
    

    def createChildren(self):
        if not self.children:
            # find the coordinates of the empty place
            # (the empty place contains a zero)
            val = self.value
            posZero = 0
            for i in xrange(len(self.goal)):
                if val[i] == '0':
                    posZero = i
                    break
            n = self.puzzleSize
            empty_cell = [posZero // n, posZero % n]          

            # determine the places where the empty cell can be moved 
            moves = self.allowedMoves(empty_cell, n)
            
            # generate all possible successor states            
            for m in moves:
                val = self.value # is a string object, so this is deep copy
                newPosZero = m[0] * n + m[1]
                # 'str' object does not support item assignment, so we need to concatenate
                val = val[:posZero] + val[newPosZero] + val[posZero+1:]
                val = val[:newPosZero] + '0' + val[newPosZero+1:]
                child = State_NPuzzle(val, self)
                self.children.append(child)
            
    def allowedMoves(self, empty_cell, n):
        moves = []
        for i in range(empty_cell[0]-1, empty_cell[0]+2):
            for j in range(empty_cell[1]-1, empty_cell[1]+2):
                if ([i,j] == empty_cell):
                    continue
                # if [i,j] is not out of bounds
                # and is vertically or horizontally aligned to the empty space 
                if ((0 <= i and i < n) and (0 <= j and j < n) 
                    and (i == empty_cell[0] or j == empty_cell[1])):
                    moves.append([i, j])
        return moves
                    
            
