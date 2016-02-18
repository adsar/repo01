from math import log, sqrt
import numpy as np


def purity_for_quizz(groundtruthAssignment, algorithmAssignment):

    purity = 0
    N = 0
    pi = []
    ni = []
    
    for r in algorithmAssignment:
        max = r[0]
        for nij in r:
            if (nij > max):
                max = nij
        p = max/float(sum(r))
        #print r, 'cluster max', max, '   purity[i] = ', p
        pi.append(p)
        ni.append(sum(r))
    
    a = np.array(ni)
    b = np.array(pi)
     
    purity = np.dot(a,b) / sum(ni)   
    return purity 

def summarize(groundtruthAssignment, algorithmAssignment, verbose):    
    sumA = []
    sumClusters = []
    sumPartitions = []
    
    partIDs = np.unique(groundtruthAssignment) #because not all labels start in zero
    clusIDs = np.unique(algorithmAssignment) #because not all centroids actually get points assigned
    
    # for each combination of Cluster and partition, count the points with matching label
    N = len(algorithmAssignment)
    for clusID in clusIDs:
        r = []
        for partID in partIDs:
            s = 0
            for i in range(N):
                if (algorithmAssignment[i] == clusID and groundtruthAssignment[i] == partID):
                    s += 1            
            r.append(s)
        
        sumA.append(r)
        sumClusters.append(sum(r))
    
    # calculate the total of each partition    
    for j in range(len(sumA[0])): 
        s = 0
        for i in range(len(sumA)):
            s += sumA[i][j]
        sumPartitions.append(s)
    if (verbose):
        print    
        print 'Number of data points N = ', N
        print 'Nij'
        print sumA
        print
        print 'Total per Cluster '
        print sumClusters
        print
        print 'Total per Part '
        print sumPartitions
        print
    
    return sumA, sumClusters, sumPartitions

def calcPurity(sumA):
    pi = []
    ni = []
    for r in sumA:
        max = r[0]
        for nij in r:
            if (nij > max):
                max = nij
        
        p = max / float(sum(r)  +0.00000000001)
        print r, 'cluster max', max, '   purity[i] = ', p
        
        pi.append(p)
        ni.append(sum(r))
    
    a = np.array(ni)
    b = np.array(pi)
    
    purity = np.dot(a, b) / sum(ni)
    return purity

def purity(groundtruthAssignment, algorithmAssignment):   

    purity = 0 
    
    sumA, x, y = summarize(groundtruthAssignment, algorithmAssignment, True) 
    purity = calcPurity(sumA)   
    
    return purity 

def NMI(groundtruthAssignment, algorithmAssignment):   

    NMI = 0
    
    # Summarization 
    N = float(len(algorithmAssignment))
    sumA, sumClusters, sumPartitions = summarize(groundtruthAssignment, algorithmAssignment, False)

    # Probability     
    P = np.array(sumA) / N 
    PC = np.array(sumClusters) / N 
    PT = np.array(sumPartitions) / N 
    print  "Probability Pi:  "
    print  P
    print  "Probability PC: " , PC
    print  "Probability PT: " , PT
    
    # Entropy
    H_C = -np.sum(PC * np.log(PC +0.00000000001))
    H_T = -np.sum(PT * np.log(PT +0.00000000001))
    print  "Entropy H_C: %f  - H_T: %f  " % (H_C, H_T)
            
    I_CT = 0.0
    for i in range(len(P)):
        for j in range(len(P[0])):
            if P[i][j] != 0.0:
                I_CT += P[i][j] * np.log(P[i][j] / ((PC[i] * PT[j])  +0.00000000001))
    print  "Entropy I_CT: %f" % (I_CT)
        
    # NMI
    NMI = I_CT / (np.sqrt(H_C * H_T +0.00000000001))
    
    return NMI
