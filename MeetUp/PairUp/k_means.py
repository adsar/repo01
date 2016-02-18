from utils import * 


def computeSSE(data, centers, clusterID):
    sse = 0 
    nData = len(data) 
    for i in range(nData):
        c = clusterID[i]
        sse += squaredDistance(data[i], centers[c]) 
        
    return sse 

def updateClusterID(data, centers):
    nData = len(data) 
    
    clusterID = [0] * nData
    
    # assign the closet center to each data point
    for i in range(len(data)):
        min = centers[0]
        minD2 = 0
        
        for j in range(len(centers)):
            d2 = squaredDistance(data[i], centers[j])
            if d2 < minD2 or j == 0:
                minD2 = d2
                min = j
                
        clusterID[i] = min
    
    return clusterID

# K: number of clusters 
def updateCenters(data, clusterID, K):
    nDim = len(data[0])
    centers = [[0.0] * nDim for i in range(K)]

    # recompute the centers 
    # If a cluster doesn't have any data points, leave it to ALL 0s
    for i in range(len(clusterID)):       
        centers[clusterID[i]] += data[i]
        
    for j in range(K):
        Nj = sum([(1 if (clusterID[i] == j) else 0) for i in range(len(clusterID))]) 
        
        Sj = [0.0] * nDim
        for x in range(nDim):
            Sj[x] = sum([(data[i][x] if (clusterID[i] == j) else 0) for i in range(len(clusterID))])
            Sj[x] /= Nj  

        centers[j] = Sj          


    return centers 

def kmeans(data, centers, maxIter = 100, tol = 1e-6):
    nData = len(data) 
    
    if nData == 0:
        return [];

    K = len(centers) 
    
    clusterID = [0] * nData
    
    if K >= nData:
        for i in range(nData):
            clusterID[i] = i
        return clusterID

    nDim = len(data[0]) 
    
    lastDistance = 1e100
    
    for iter in range(maxIter):
        clusterID = updateClusterID(data, centers) 
        centers = updateCenters(data, clusterID, K)
        
        curDistance = computeSSE(data, centers, clusterID) 
        if lastDistance - curDistance < tol or (lastDistance - curDistance)/lastDistance < tol:
            print "# of iterations:", iter 
            print "SSE = ", curDistance
            return clusterID
        
        lastDistance = curDistance
        
    print "# of iterations:", iter 
    print "SSE = ", curDistance
    return clusterID

