'''
Created on Oct 10, 2014

@author: adrian
'''
import sys
import numpy as np

def powerIteration(M, numIter):
    epsilon = 1.0/10000
    # print 'epsilon = ', epsilon
    n = M.shape[1]
    r = np.array(np.ones(n,float)/n)

    for _ in range(numIter):
        r_prev = r
        r = np.dot(M, r)
        #print
        #print 'iteration ', i
        #print r, '  - sum(r) = ', sum(r)

        #print 'L1 norm of (r - r_prev) = ', d
        d = sum(np.absolute(r - r_prev))
        if (d <= epsilon):
            #print 'Power iteration ', i, '   - L1 norm of (r - r_prev) is <=  epsilon (', epsilon, ')'
            break
    return r

def googleFormula_wrong(M, beta, numIter):
    epsilon = 1.0/10000
    # print 'epsilon = ', epsilon

    n = M.shape[1]
    r0 = np.array(np.ones(n,float)/n)
       
    # rule to fix Dead Ends: detect pages with zero out-degree and 
    # assign them a uniform distribution of linking to every page in the web 
    # Pre-processing the matrix:
    # THIS IMPLEMENTATION IS WRONG BECAUSE M is HUGE and SPARSE, THIS LOOP TAKES FOREVER 
    # AND PRODUCES A LESS SPARSE MATRIX
    for j in range(n):
        if (sum(M[:,j]) == 0):
            M[:,j] = r0

    r = r0
    for _ in range(numIter):
        r_prev = r
        
        # rule to fix Spider Traps: random jumps to any other node with probability (1 - beta)
        r = beta * np.dot(M, r) + (1 - beta) * r0
        #print
        #print 'iteration ', i
        #print r, '  - sum(r) = ', sum(r)

        #print 'L1 norm of (r - r_prev) = ', d
        d = sum(np.absolute(r - r_prev))
        if (d <= epsilon):
            #print 'Google (wrong implementation) formula iteration ', i, '   - L1 norm of (r - r_prev) is <=  epsilon (', epsilon, ')'
            break
    return r

def googleFormula_theoretical(M, beta, numIter):
    epsilon = 1.0/10000
    # print 'epsilon = ', epsilon
    
    n = M.shape[1]
    r0 = np.array(np.ones(n,float)) / n
    
    # THIS IS THE RIGHT IMPLEMENTATION
    # We implement both rules at the same time by calculating the Google Matrix A
    # 1. Rule to fix Spider Traps: random jumps to any other node with probability (1 - beta)
    # 2. Rule to fix Dead Ends: detect pages with zero out-degree and 
    # assign them a uniform distribution of linking to every page in the web
    # THIS IMPLEMENTATION IS UNREALISTIC, BECAUSE THE MATRIX A IS NOT SPARSE (IMPOSSIBLE MEMORY REQUIREMENT!) 
    A = beta * M + (1 - beta) * np.ones(M.shape, float) / n

    r = r0
    for _ in range(numIter):
        r_prev = r      
        r = np.dot(A, r)
        #print
        #print 'iteration ', i
        #print r, '  - sum(r) = ', sum(r)

        #print 'L1 norm of (r - r_prev) = ', d
        d = sum(np.absolute(r - r_prev))
        if (d <= epsilon):
            #print 'Google formula iteration ', i, '   - L1 norm of (r - r_prev) is <=  epsilon (', epsilon, ')'
            break
    return r


def googleFormula_realistic(M, beta, numIter, r0 = None):
    epsilon = 1.0/10000
    # print 'epsilon = ', epsilon
    
    if (r0 == None):
        n = M.shape[1]
        r0 = np.array(np.ones(n,float)) / n
    
    # THIS IS THE RIGHT IMPLEMENTATION
    # We implement both rules at the same time by calculating the Google Matrix A
    # 1. Rule to fix Spider Traps: random jumps to any other node with probability (1 - beta)
    # 2. Rule to fix Dead Ends: detect pages with zero out-degree and 
    # assign them a uniform distribution of linking to every page in the web 
    # WE DONT NEED TO ACTUALLY MATERIALIZE THE MATRIX A
    # keeps M sparse, 10 links per node, approx 10N is the actual size of M 

    r = r0
    for _ in range(numIter):
        r_prev = r      
        r = beta * np.dot(M, r) + (1 - beta) * r0
        
        # re-normalize:
        # reinsert any leaked probability due to zero columns in M
        sumr = sum(r)
        if (sumr < 1):
            r += (1 - sumr) * r0
        #print
        #print 'iteration ', i
        #print r, '  - sum(r) = ', sum(r)

        #print 'L1 norm of (r - r_prev) = ', d
        d = sum(np.absolute(r - r_prev))
        if (d <= epsilon):
            #print 'Google formula iteration ', i, '   - L1 norm of (r - r_prev) is <=  epsilon (', epsilon, ')'
            break
    return r

def compareRankFunctions(M):
    numIter = 100
    beta = 0.85
    print M
    
    ranks = powerIteration(M, numIter)
    print 'PowerIteration Ranks = ', np.round(ranks, 3)
    
    googleWRanks = googleFormula_wrong(M, beta. numIter)
    print 'Google Ranks (worst implementation) = ', np.round(googleWRanks, 3)
    
    googleTRanks = googleFormula_theoretical(M, beta, numIter)
    print 'Google Ranks (theoretical implementation) = ', np.round(googleTRanks, 3)

    googleRRanks = googleFormula_realistic(M, beta, numIter)
    print 'Google Ranks (realistic implementation) = ', np.round(googleRRanks, 3)


def classExamples():
    print 'The stochastic web matrix M (is column-stochastic)'
    print 'The Ranks vector is also stochastic (is a probability distribution)'
    print 'The Flow Equation of the Power Iteration is r = M . r   , R is an Eigenvector (aguen)'
    M = np.array([[.5, .5, 0.0], [.5, 0.0, 1.0], [0.0, .5, 0.0]])
    print 
    print 'Power Iteration converges if M is stochastic, aperiodic and irreducible'
    compareRankFunctions(M)
    M = np.array([[.5, .5, 0.0], [.5, 0.0, 0.0], [0.0, .5, 1.0]])
    print 
    print 'M has a spider trap - a node that links only to itself (violates aperiodicity).'
    print 'Spider traps, trap the random walker. After enough iterations,'
    print 'a bot (web spider) will be in the trap node with probability 1'
    print 'W 1 in the main diagonal means that M has a spider trap.'
    compareRankFunctions(M)
    M = np.array([[.5, .5, 0.0], [.5, 0.0, 0.0], [0.0, .5, 0.0]])
    print 
    print 'M has a dead end - a node with no outgoing links (not even to itself)'
    print 'Dead ends, leak the probability in every iteration and eventually,'
    print 'all the ranks converge to zero.'
    print 'This just means that the bot will be jumping nowhere.'
    print 'A column with only zeroes means that M has a dead end (violates stochasticity)'
    compareRankFunctions(M)



def hw1q1():
    numIter = 100
    beta = 0.7
    M = np.array([[0.0, 0.0, 0.0], [.5, 0.0, 0.0], [0.5, 1.0, 1.0]])
    print M
    
    ranks = powerIteration(M, numIter)
    print 'PowerIteration Ranks = ', np.round(ranks, 3)
    
    googleRRanks = googleFormula_realistic(M, beta, numIter)
    r = np.round(googleRRanks, 3)
    print 'Google Ranks = ', r
    print 'Google Ranks ( x 3) = ', r * 3
    print 'a + b = ', (r[0] + r[1]) * 3
    print 'b + c = ', (r[1] + r[2]) * 3
    print 'a + c = ', (r[0] + r[2]) * 3




def hw1q2():
    numIter = 100
    beta = 0.85
    M = np.array([[0.0, 0.0, 1.0], [.5, 0.0, 0.0], [0.5, 1.0, 0.0]])
    print M
    
    ranks = powerIteration(M, numIter)
    print 'PowerIteration Ranks = ', np.round(ranks, 3)
    
    googleRRanks = googleFormula_realistic(M, beta, numIter)
    r = np.round(googleRRanks, 3)
    print 'Google Ranks = ', r
    a = r[0]
    b = r[1]
    c = r[2]

    print 'b = .475a + .05c'
    print b, ' = ', .475 * a + .05 * c

    print '.85a = c + .15b'
    print .85 * a,' = ', c + .15 * b

    print '.95b = .475a + .05c'
    print .95 * b, ' = ', .475 * a + .05 *c

    print '.85c = b + .575a'
    print .85 * c, ' = ', b + .575 * a
    



def hw1q3():
    numIter = 5
    beta = 1.0
    M = np.array([[0.0, 0.0, 1.0], [.5, 0.0, 0.0], [0.5, 1.0, 0.0]])
    print M
    
    ranks = powerIteration(M, numIter)
    print
    print 'PowerIteration Ranks = ', np.round(ranks, 3)
    
    n = M.shape[1]
    r0 = np.array(np.ones(n,float))

    googleRRanks = googleFormula_realistic(M, beta, numIter, r0)
    r = np.round(googleRRanks, 3)
    print 'Google Ranks = ', r
    print
    print 5.0/8, 9.0/16, 13.0/8


    


def main(argv):
    #classExamples()
    
    hw1q1()
    hw1q2()
    hw1q3()
    
    
            
if __name__ == '__main__':
    main(sys.argv[:])