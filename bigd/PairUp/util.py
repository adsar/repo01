# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 23:33:18 2016

@author: adrian
"""

import numpy as np

def squared_distance(v1, v2):
    a1 = np.array(v1)
    a2 = np.array(v2)
    return sum((a2-a1)**2)

def vector_mean(v):
    a = np.array(v)
    ret = np.mean(a, axis=0)
    return ret