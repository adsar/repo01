import sys

def main(dishFile, sentFile, dishSentFile):
    dishes = []
    dishSent = {}
    dishFreq = {}
    count = 0
    with open (dishFile , 'r') as f:
        for line in f.readlines():
            count += 1
            if count > 1:
                d = line.rstrip('\n')
                dishes.append(d)
                dishSent[d] = 0
                dishFreq[d] = 0 
            if count > 30: break

    #Calculate the sentiment and the frequency of each dish
    count = 0
    with open (sentFile , 'r') as f:
        for line in f.readlines():
            if count > 100000: break
            row = line.rstrip('\n').split("\t")
            
            # Apply the sentiment of each review to each dish included in it, 
            # accumulating the sentiment and the frequency for each dish:
            for d in dishes:
                if d in row[0]:
                    dishSent[d] += int(row[1])
                    dishFreq[d] += 1     
                    count += 1
        # Normalize
        # - total dish sentiment by the dish's review frequency (how many reviews contain it)
        maxSent = 0
        minSent = 10
        for d in dishes:
            if d in dishSent:
                dishSent[d] = dishSent[d]/(dishFreq[d])
                if dishSent[d] > maxSent: maxSent = dishSent[d]
                if dishSent[d] < minSent: minSent = dishSent[d]

    rankedDishes = []
    with open(dishSentFile, 'w') as f:
        for d in dishes:
            rankedDishes.append([d, dishFreq[d], dishSent[d]])

    rankedDishes = sorted(rankedDishes, key=lambda r: "%f %f %s" % (float(r[1])/count, r[2], r[0]), reverse=True)


    with open(dishSentFile, 'w') as f:
        for r in rankedDishes:
            f.write("%s:%d:%d\n" % (r[0], r[1], 1+4*(r[2]-minSent)/(maxSent-minSent)))
# -----------------------------------------------------------
# this file can act as main program and as import module
if __name__=="__main__":
    args = sys.argv[1:]       
    main(args[0], args[1], args[2])
