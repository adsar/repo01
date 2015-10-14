'''
Created on Oct 15, 2014

@author: adrian
'''

import numpy as np
import copy
import pandas as pd
import datetime as dt
from pandas.algos import ffill_by_group



if __name__ == '__main__':
    
    labels = ['1', '2', '3', '4']
    colnames = ['a', 'b', 'c']
    r = len(labels)
    c = len(colnames)
    dat = np.zeros(r * c)   
    
    data = pd.DataFrame(np.reshape(dat, (r, c)), index=labels, columns=colnames)
    data['a'].fillna(1.0)
    data['b'].fillna(2.0)
    data['c'].fillna(3.0)
    

    print data[0:1]
    