import sys
from LoadData import * 
from k_means import * 
from evaluation import * 

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "[usage] <data-file> <ground-truth-file>"
        exit(1) 

    dataFilename = sys.argv[1]
    groundtruthFilename = sys.argv[2]
    print  "points X: %s   -   labels Y: %s " % (dataFilename, groundtruthFilename)
        
    data = loadPoints(dataFilename) 
    groundtruth = loadClusters(groundtruthFilename) 
    
    nDim = len(data[0]) 
   
    #K = 2  # Suppose there are 2 clusters 
    K = len(np.unique(groundtruth)) # number of parts in ground truth   

        
    for X in range(2,6):
        print        
        print        
        print "------------------------------------------------------------------------"    
        print  "Ground Truth Partitions K = %d   -    Initial Centroids X = %d " % (K, X)  
        print np.unique(groundtruth)       
        centers = [] 
        for i in range(X):
            centers.append(data[i])   
        
        results = kmeans(data, centers) 
        
        R = len(np.unique(results)) # number of clusters (centroids with at least one point assigned)
        print  "Resulting Clusters R = %d " % (R)
        print np.unique(results)            
        print "------------------------------------------------------------------------"  
            
        res_Purity = purity(groundtruth, results) 
        res_NMI = NMI(groundtruth, results) 
        
        print "Purity =", res_Purity
        print "NMI = ", res_NMI
    

