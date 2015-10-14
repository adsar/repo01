'''
Created on Oct 11, 2014

@author: adrian
'''

import sys
import numpy as np

def bruteForceFactors(n):
    li_factors = []
    for i in range(2, int(np.sqrt(n)) + 1):
        while(n % i == 0):
            li_factors.append(i)
            n /= i 
  
    if (n > 1):
        li_factors.append(n) 

    return li_factors


def distinctFactors(n):
    li_factors = bruteForceFactors(n)
    print #print 'Prime Factors of ', n, ' : ', li_factors
    li_nonRep_factors = []
    for f in li_factors:
        if f not in li_nonRep_factors:
            li_nonRep_factors.append(f)
    
    print
    print 'Distinct prime factors of ', n, ' : ', li_nonRep_factors
    return li_nonRep_factors


def mapper(numbers):
    mapping = []
    for i in numbers:
        primeFactors = distinctFactors(i)
        for p in primeFactors:
            mapping.append([p, i])

    return mapping

def reducer(pairs):
    # calculates the sum of all multiples of each factor
    
    # use a dictionary to summarize
    sums = {}
    
    for pair in pairs:
        factor = pair[0]
        multiple = pair[1]

        if factor not in sums:
            sums[factor] = 0
        
        sums[factor] += multiple
    
    return  sums   
        
    
def main(argv):
    numbers = [15, 21, 24, 30, 49]

    pairs = mapper(numbers)
    print
    print pairs
     
    reduction = reducer(pairs) 
    print
    print reduction   
       
if __name__ == '__main__':
    main(sys.argv[:])
