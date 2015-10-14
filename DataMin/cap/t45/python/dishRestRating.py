import sys

def main(dishFile, reviewFile, dishRestRatingFile):
    dishes = []
    restaurants = {}
    dishRestRating = {}
    dishRestFreq = {}
    count = 0
    with open (dishFile , 'r') as f:
        for line in f.readlines():
            count += 1
            if count > 1:
                d = line.rstrip('\n')
                dishes.append(d)
                dishRestRating[d] = {}
                dishRestFreq[d] = {}
            if count > 30: break

    #Calculate the rating and the frequency of each dish-restaurant tuple
    count = 0
    with open (reviewFile , 'r') as f:
        for line in f.readlines():
            count += 1
            if count > 1000000: break
            row = line.rstrip('\n').split("\t")
            if len(row) != 3: continue
            # Apply the rating of each review to each dish included in it, 
            # accumulating the rating and the frequency for each dish:
            for d in dishes:
                if d in row[0]:
                    restId = row[2]
                    restaurants[restId] = 1
                    if restId in dishRestRating[d]:
                        dishRestRating[d][restId] += int(row[1])
                        dishRestFreq[d][restId] += 1
                    else:
                        dishRestRating[d][restId] = int(row[1])
                        dishRestFreq[d][restId] = 1
   
        # Normalize
        # - total dish restaurant rating by the dish-restaurant review frequency (how many reviews contain it)
        for d in dishes:
            if d in dishRestRating:
                for r in restaurants:
                    if r in dishRestRating[d]:
                        dishRestRating[d][r] = dishRestRating[d][r]/dishRestFreq[d][r]
                    else:
                        dishRestRating[d][r] = 0
                        dishRestFreq[d][r] = 1

    rankedDishRestaurants = []
    for d in dishes:
        for r in restaurants:
            rankedDishRestaurants.append([d, r, dishRestFreq[d][r], dishRestRating[d][r]])

    rankedDishRestaurants = sorted(rankedDishRestaurants, key=lambda r: "%f %f %s %s" % (r[2]/count, r[3], r[0], r[1]), reverse=True)

    with open(dishRestRatingFile, 'w') as f:
        for r in rankedDishRestaurants:
            f.write("%s\t%s\t%d\t%d\n" % (r[0], r[1], r[2], r[3]))
# -----------------------------------------------------------
# this file can act as main program and as import module
if __name__=="__main__":
    args = sys.argv[1:]       
    main(args[0], args[1], args[2])
