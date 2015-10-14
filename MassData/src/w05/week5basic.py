'''
Created on Nov 4, 2014

@author: adrian
'''

import numpy as np
import math 

def distance(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def assign_cluster(points, centroids):
    for j in range(0, len(points)):
        #include yellow and green points
        p1 = [points['x'][j], points['y'][j]]
        cluster = 0
        dist = distance(p1, centroids[cluster])
        for c in range(1, len(centroids)):
            p2 = centroids[c]
            d = distance(p1, p2)
            if d < dist:
                dist = d
                cluster = c
        
        if points['c'][j] != cluster:
            print "point (%d, %d) changed from cluster %s to cluster %s" % (points['x'][j], points['y'][j], points['c'][j], cluster)       
        
        points['c'][j] = cluster
        points['d'][j] = dist
        

def init():
    points = np.array([(28, 145, "y", 0, 0.0), (65, 140, "y", 0, 0.0), (50, 130, "y", 0, 0.0), (25, 125, "g", 0, 0.0), (55, 118, "y", 0, 0.0), (38, 115, "y", 0, 0.0), (44, 105, "g", 0, 0.0), (29, 97, "g", 0, 0.0), (50, 90, "y", 0, 0.0), (63, 88, "y", 0, 0.0), 
            (43, 83, "y", 0, 0.0), (35, 63, "g", 0, 0.0), (55, 63, "g", 0, 0.0), (50, 60, "y", 0, 0.0), (42, 57, "g", 0, 0.0), 
            (23, 40, "g", 0, 0.0), (64, 37, "g", 0, 0.0), (50, 30, "y", 0, 0.0), (33, 22, "g", 0, 0.0), (55, 20, "g", 0, 0.0)], 
        dtype=[('x', 'i8'), ('y', 'i8'), ('color', '|S1'), ('c', 'i4'), ('d', 'f8.1')])
    centroids = {}
    cluster = 0
    for i in range(0, len(points)):
        if points['color'][i] == "g":
            centroids[cluster] = [points['x'][i], points['y'][i]]
            cluster += 1
    
    return points, centroids


def compute_centroids(points, centroids):
    for c in range(1, len(centroids)):
        x = np.average(points['x'][points['c'] == c])
        y = np.average(points['y'][points['c'] == c])
        centroids[c] = [x, y]

def print_status(points, centroids):
    print 
    print 'points'
    print points
    print 'centroids'
    for c in range(1, len(centroids)):
        p2 = centroids[c]
        print c, p2
    print
    
def w5Bq1():
  
    points, centroids = init()
    print_status(points, centroids)  
        
    # recomputation pass 1
    assign_cluster(points, centroids)
    compute_centroids(points, centroids)
    print_status(points, centroids)  
  
  
def w5Bq2():
    C1 = np.array([5, 10])
    C2 = np.array([20, 5])
    
    a1 = np.array([[6,7], [11,4], [14,10], [23,6]])
    a2 = np.array([[3,15], [13,7], [11,5], [17,2]])
    a3 = np.array([[3,3], [10,1], [13,10], [16,4]])
    a4 = np.array([[7,8], [12,5], [13,10], [16,4]])
    
    for a in [a1, a2, a3, a4]:
        y_vert = assign(np.array([C1, C2]), a[:2,:])
        b_vert = assign(np.array([C1, C2]), a[2:,:])
        print
        print a 
        print y_vert   
        print b_vert  
        if (y_vert[0] == 4 and b_vert[1] == 4)\
        or (y_vert[1] == 4 and b_vert[0] == 4):
            print '** Initial Clustering Successful !! **'
            print


def assign(centroids, rec):
    counters = np.array([0, 0])
    UL = np.array([rec[0,0], rec[0,1]])
    UR = np.array([rec[1,0], rec[0,1]])
    LL = np.array([rec[0,0], rec[1,1]])
    LR = np.array([rec[1,0], rec[1,1]])
    vertices = [UL, UR, LL, LR]
    for v in vertices:
        cluster = select_cluster(centroids, v)
        counters[cluster] += 1
    
    return counters   

def select_cluster(centroids, v):
    d0 = distance(v, centroids[0])
    d1 = distance(v, centroids[1])
                  
    cluster = 0 if d0 <= d1 else 1
    return cluster

def main():
    #Clustering
    w5Bq1()
    w5Bq2()
    
    #Advertisement
    
    
    #Clustering

if __name__ == '__main__':
    main()