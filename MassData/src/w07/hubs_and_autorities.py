'''
Created on Nov 18, 2014

@author: adrian
'''
import numpy as np

def main():
    L = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    LT = np.array([[0, 1, 0, 0], [1, 0, 0, 0], [1, 0, 0, 1], [0, 0, 1, 0]])
    h = np.array([1.0, 1.0, 1.0, 1.0])
    a = np.array([1.0, 1.0, 1.0, 1.0])
    

    error = 0.0001
    print
    print 'Hubs and Authorities'
    print LT
    
      
    for i in range(100):
        print
        print 'Iteration %d' % (i)
        a1 = np.dot(LT,h)
        print '    a = [%5.4f, %5.4f, %5.4f, %5.4f]    normalization: max(h) = %5.4f' % (a1[0], a1[1], a1[2], a1[3], np.max(a1))       
        a1 = a1 / np.max(a1)
        print '    a = [%5.4f, %5.4f, %5.4f, %5.4f]' % (a1[0], a1[1], a1[2], a1[3])        
        da = np.max(np.abs(a - a1))
        
        h1 = np.dot(L,a1)
        print '    h = [%5.4f, %5.4f, %5.4f, %5.4f]    normalization: max(h) = %5.4f' % (h1[0], h1[1], h1[2], h1[3], np.max(h1))
        h1 = h1 / np.max(h1)         
        print '    h = [%5.4f, %5.4f, %5.4f, %5.4f]' % (h1[0], h1[1], h1[2], h1[3])
        dh = np.max(np.abs(h - h1))        
        print
               
        print '    max delta h, a: %5.4f %5.4f' % (dh, da)
        if da < error and dh < error:
            break
        a = a1
        h = h1   
        
        if h[2] == 3.0/5: 
            print '1 ***'
        if a[1] == 1.0/8: 
            print '2 ***'
        if h[2] == 1: 
            print '3 ***'
        if a[3] == 1.0/5: 
            print '4 ***'
    
    
if __name__ == '__main__':
    main()