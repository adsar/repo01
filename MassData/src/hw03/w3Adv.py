'''
Created on Oct 28, 2014

@author: adrian
'''



#def q2():
    # can be computed with www.wolframalpha.com
    # The matrix is input as follows:
    # eigenvectors{{2,-1,-1,0,0,0},{-1,3,0,-1,0,-1},{-1,0,2,-1,0,0},{0,-1,-1,3,-1,0},{0,0,0,-1,2,-1},{0,-1,0,0,-1,2}}
    # the 2 smaller eighenvector is:
    # v5 = (-1, 0, -1, 0, 1, 1)
    # this makes 3 clusters: (1, 3), (2, 4), (5, 6)
def q3():
    stream_length = 75.0
    possible_elements = 10
    
    # calculated directly from the stream by definition formula
    second_momentum = 5 * 8**2 + 5 * 7**2
    
    # estimation by Flagolet-Martin
    print 'second momentum = %d' % (second_momentum)
    close_m = ((second_momentum / stream_length) + 1) / 2
    print 'm ~ %d' % (int(close_m))
    close_x = stream_length - possible_elements * (close_m - 1)
    print 'x ~ %d' % (int(close_x))

    # test for the candidate answers of multiple-choice
    l = [46, 43, 33, 49]
    for x in l:
        m = 1 + (stream_length - x) / possible_elements
        est = stream_length * (2 * m - 1)
        print 'x=%d, m=%d, est=%d' % (x, m, est)
    print
    
def q4():
    for e in range(1, 11):
        h = (3 * e + 7) % 11
        comment = ''
        if h == 4:
            comment = '(tail = 2)'
        elif h == 8:
            comment = '(tail = 3)'
            
        print "H(%d) = %d   %s" % (e, h, comment)
if __name__ == '__main__':
    #q2()
    q3()
    q4()