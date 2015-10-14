'''
Created on Oct 20, 2014

@author: adrian
'''

import numpy as np
from numpy.linalg import norm
import pandas as pd

def cosine_distance(u, v):
    return np.dot(u, v) / norm(u) * norm(v)

def question02():
    col = ['A1', 'A2', 'A3', 'A4', 'A5', 'rating']
    item = ['A', 'B', 'C']
    value = np.array([1, 0, 1, 0, 1, 2, 1, 1, 0, 0, 1, 6, 0, 1, 0, 1, 0, 2])
    value = value.reshape(len(item), len(col))
    value = value.astype(float)
    df_profile = pd.DataFrame(value, index=item, columns=col)
    print df_profile
    
    ranking_scale_factor = [0.0, 0.5, 1.0, 2.0]
    
    for rsf in ranking_scale_factor:
        a = np.array(df_profile)
        # apply scale factor to each column
        scale_factor = np.array([1.0, 1.0, 1.0, 1.0, 1.0, rsf])
        a = a * scale_factor[None, :]

        print
        print 'Normalized with rating scale factor of %s' % (rsf)
        print a
        
        for i in range(len(item) - 1):
            for j in range(i + 1, len(item)):
                cosdist = cosine_distance(a[i,:], a[j,:])
                print 
                print 'CosineDistance(%s, %s) =  %s' % (item[i], item[j], cosdist)
    
def main():
    question02()

if __name__ == '__main__':
    main()