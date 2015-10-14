from utils import * 
from math import exp 

def RBF(x_i, x_j, sigma):
    d2 = squaredDistance(x_i, x_j)
    Sigma2 = sigma*sigma
    RBF = exp(-d2/(2*Sigma2))
    return RBF
    
def kernel(data, sigma):
    nData = len(data)
    Gram = [[0] * nData for i in range(nData)] 
    # TODO
    # Calculate the Gram matrix 
    for i in range(len(Gram)):
        for j in range(len(Gram[0])):
            Gram[i][j] = RBF(data[i], data[j], sigma)

    return Gram 


