# This Python file uses the following encoding: utf-8
'''
Created on Nov 18, 2014

@author: adrian
'''
import numpy as np

def w07_basic_q1():
    '''
    Compute the Topic-Specific PageRank for a given link topology.
    Teleport set S = {1, 2}, with the following distribution: the weight of node 1 is twice the weight of node 2.
    (1 - beta) = 0.3 
    
    Using the TSPR method, and power iteration with stochastic matrix M to find the principal eighenvector  
    '''
    M = np.array([[0,1,0,0],[0.5, 0, 0, 0],[0.5, 0, 0, 1],[0,  0, 1, 0]])
    eS = np.array([2.0/3, 1.0/3, 0, 0])   # a prob distribution where p(1) is twice p(2)
    beta = 0.7
    v = np.array([.25, .25, .25, .25])
    error = 0.0001
    print
    print 'Topic-Specific PageRank'  
    for i in range(100):
        print
        print 'TSPR Iteration %d' % (i)
        print '    v = [%5.4f, %5.4f, %5.4f, %5.4f]' % (v[0], v[1], v[2], v[3])
        print '    verification: sum(v) = %5.4f' % (sum(v))
        v1 = beta* np.dot(M, v) + (1-beta) * eS
        d = np.max(np.abs(v - v1))
        print '    max delta: %5.4f' % (d)
        if d < error:
            break
        v = v1
        

def w07_basic_q2():
    '''
    Compute the coefficients of the form that calculates the page rank 
    in a 2-tiered spam farm:
        y = ax + b(m/n) + c(k/n)
    
    Here is an outline of the solution: 
    Use w as the PageRank of each second-tier page and z as the PageRank of each supporting page. 
    You can write three equations, 
        one for y in terms of z, 
        one for w in terms of y, 
        and one for z in terms of w. 
    For example, 
        y equals x (the PageRank from outside) 
                plus all the untaxed PageRank of each of the m supporting pages (a total of βzm), 
                plus its share of the tax (which is (1-β)/n). 
    
    Discover the equations for w and z, 
    then substitute these in the equation for y to get an equation for y in terms of itself, 
    from which you can solve for y.
    
    
    SOLUTION:
        y: page rank of the target page t
        w: PageRank of each second-tier page
        z: PageRank of each supporting page
        1) y in terms of z: y = x + β z m + (1-β)/n
        2) w in terms of y: w = β y / k + (1-β)/n
        3) z in terms of w: z = β w / (m/k) + (1-β)/n
        
        substituting z and w, from (3) and (2) (in that order) in (1):
        (1)         y = x + β z m + (1-β)/n 
        apply (3)   y = x + β [β w / (m/k) + (1-β)/n] m + (1-β)/n
        apply (2)   y = x + β [β [β y / k + (1-β)/n] / (m/k) + (1-β)/n] m + (1-β)/n
                    y = x + β [[β^2 y/k + β(1-β)/n] * (k/m) + (1-β)/n] m + (1-β)/n
                    y = x + β [β^2 y/m + β(1-β)k/nm + (1-β)/n] m + (1-β)/n
                    y = x + [β^3 y/m + β^2(1-β)k/nm + β(1-β)/n] m + (1-β)/n
                    y = x + β^3 y + β^2(1-β)k/n + β(1-β)m/n + (1-β)/n
                    
                    y - β^3 y = x + β^2(1-β)k/n + β(1-β)m/n + (1-β)/n 
                    y = x/(1-β^3) + β^2(1-β)/(1-β^3) k/n + β(1-β)/(1-β^3) m/n + (1-β)/(1-β^3) 1/n
                    
                    Discard the last term (~ 1 divided by n) and obtain the form y = ax + b(m/n) + c(k/n)
                    
                    a = 1/(1-β^3)
                    b = β(1-β)/(1-β^3)
                    c = β^2(1-β)/(1-β^3)   
    
    '''
    beta = 0.85
    a = 1.0/(1-beta**3)
    b = beta*(1-beta)/(1-beta**3)
    c = beta**2*(1-beta)/(1-beta**3)
    
    print
    print 'Spam Farm Analysis'  
    print 'beta = %6.4f' % (beta)
    print 'y = ax + b m/n + c k/n'  
    print 'a = 1/(1-β^3)) = %6.4f' % (a)
    print 'b = β(1-β)/(1-β^3) = %6.4f' % (b)
    print 'c = β^2(1-β)/(1-β^3) = %6.4f' % (c)
        
    
    

def main():
    w07_basic_q1()
    print
    print
    w07_basic_q2()


if __name__ == '__main__':
    main()