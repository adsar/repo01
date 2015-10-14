4: Dish ranking
===================
Input: 
 - all the dishes of a Cuisine 
   (output of task 3)

 - all the reviews of a cuisine, not clean and stemmed!!


Feature Extraction
------------------
Feature Selection
Features used for ranking the dishes
Feature 1: Sentiment Ranking
Feature 2: Frequency (popularity)

Data Processing
 - Calculate a sentiment ranking for every review:

 - Calculate the sentiment and the frequency of each dish
 	- Apply the sentiment of each review to each dish included in it, accumulating the sentiment and the frequency for each dish:
	   for rs in reviewSent:
	     for d in dishes:
	        if d in rs[0]:
				dishSent[d] += rs[1]
	    		dishFreq[d] += 1	 
	 - Normalize total dish sentiment by the dish's review frequency (how many reviews contain it)
	 - Normalize the dish's review frequency by the total number of reviews
		dishFreq = {}
	    for d in dishes:
			dishSent[d] = dishSent[d]/(dishFreq[d]+1)
			dishFreq[d] = dishFreq[d]/len(reviewSent)
            
Visualization of results
 - Bar chart of dish frequencies with color-coded sentiment
 - Clicking on a bar opens the 5.1 visualization



5. Suggest restaurants for a dish

Feature Selection
Data features used for restaurant ranking (depending of the dish)
Feature 1: Frequency (popularity)
Feature 2: Star Rating

Data Processing
- Frequency
  For each restaurant in the cuisine (from the Business table, filtering by category=Indian)
  count the number of reviews that mention each dish, 
  and store it in a hash table (python dictionary) for random access.
  Structures used:
   - restaurantDishFreq[restId][dish]

- Star Rating
  For each restaurant in the cuisine (from the Business table, filtering by category=Indian)
  read the star rating and store it in a hash table (python dictionary) for random access.
  Structures used:
   - restaurantStarRating[restId]

Save results in a text file for visualization
   - restautrant_dish_freq.txt : contains tuples of the format <restaurantId, dish, freq>
  
Visualization of results and selection UI
 - Bar chart of restaurants ordered by frequency, with color-coded Star rating
 - Click on a bar to display the restaurant address


--------------------------------------------------------------------------------------
Main commands
> cd /media/coursera/data/as/courses/DataMin/cap/t45

Get dishes for a cuisine
> python python/processYelpRestaurants.py --cuisine
## now also outputs a json wihth the business json objects for this cuisine
## because the complete  business fileis 24 mb and made javascipt 'open' fail silently

Calculate a sentiment ranking for every review:
> java -jar sentimentAnalysis.jar ./data/all/categories/Indian.txt ./data/all/Indian_sent.txt 

Calculate the sentiment and the frequency of each dish
> python python/dishSent.py ./data/all/indian_dishes.txt ./data/all/Indian_sent.txt ./data/all/indian_dish_sent.txt

Calculate the star rating and the frequency of each restaurant-dish pair
> python python/dishRestRating.py ./data/all/indian_dishes.txt ./data/all/categories/Indian_review.txt ./data/all/indian_dish_rest_rating.txt


# visualize 
# Right-click on the page and select 'inspect element' to open the Web Kit (debugger)
chromium-browser --allow-file-access-from-files ./js/cap_t4_dish_ranking.html
chromium-browser --allow-file-access-from-files ./js/cap_t5_rest_for_dish.html?dish=aloo%20gobi


