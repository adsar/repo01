'''
Created on May 20, 2015

@author: adrian
'''
from evaluation import * 

if __name__ == '__main__':
    #groundtruth = [100, 50, 50]
    #results = [[50, 0, 10], [40, 10, 10], [10, 40, 30]]

    groundtruth = [50., 70, 80]
    results = [[20, 30, 10], [30, 40, 10], [0, 0, 60]]
    
    res_Purity = purity(groundtruth, results) 
    
    print "Purity =", res_Purity