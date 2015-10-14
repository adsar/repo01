import math
import json
import pickle
import random
from gensim import models
from gensim import matutils
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from time import time
from nltk.tokenize import sent_tokenize
import glob
import argparse
import os
import shutil

path2files="/media/coursera/data/yelp_dataset_challenge_academic_dataset/"
path2buisness=path2files+"yelp_academic_dataset_business.json"
path2reviews=path2files+"yelp_academic_dataset_review.json"
path2sampledOutput="./data/"
path2Allcategories = path2sampledOutput + "/all/categories/"
r = 'Restaurants'
max_num_cuisines = 30
min_num_reviews_per_cat = 30
max_num_reviews = 100000


def readFilteredReviews(restaurantIDs, ratingFilter):
    restID2filteredRevID = {}
    totalFilteredReviews = 0
    print "reading IDs of "+ratingFilter+" reviews for each restaurant"
    with open (path2reviews, 'r') as f:
        for line in f.readlines():
            review_json = json.loads(line)
            # DOUBT:
            # in the input file, some reviews may be stored over multiple lines
            # the above reads only one line, is it missing all the multi-line reviews?
            
            # only consider reviews for restaurants (exclude other business)
            if review_json['business_id'] in restaurantIDs:
                # filter reviews by rating
                # rating can be negative=(1, 2), neutral=(3) or positive=(4, 5)
                if ratingFilter=='positive' and not (review_json['stars']>3):
                    continue
                if ratingFilter=='negative' and not (review_json['stars']<=3):
                    continue
                # maintain a map of review_ids for each restaurant
                totalFilteredReviews += 1
                if review_json['business_id'] in restID2filteredRevID:
                    restID2filteredRevID[ review_json['business_id'] ].append(review_json['review_id'])
                else:
                    restID2filteredRevID[ review_json['business_id'] ] = [ review_json['review_id'] ]
    # save the map Restaurant-to-Review in a intermediate result file for eventual future use (uncomment if needed)
    # with open('data_restID2filteredRevID.pickle', 'wb') as f:
    #    pickle.dump(restID2filteredRevID,f)
    return restID2filteredRevID, totalFilteredReviews

def main(save_sample, save_categories):
    categories = set([])
    restaurantIDs = set([])
    catID2restID = {}
    rest2rate={}
    
    # read the list of shops
    print "reading restaurant table: categories and rating"
    with open (path2buisness, 'r') as f:
        for line in f.readlines():
            business_json = json.loads(line)
            bjc = business_json['categories']
            #cities.add(business_json['city'])
            
            # select those shops that cointain 'Restaurant' amongst their categories
            if r in bjc:
                # the additional categories that the restaurant has identify the 'Cuisine'
                # we are asked to identify the top 10 Cuisines,
                # so we are only interested in shops that belongs to more categories besides 'Restaurant'
                if len(bjc) > 1:
                    # keep a set with all the restaurant ids
                    restaurantIDs.add(business_json['business_id'])               
                    # keep the rating in a hash table
                    rest2rate[ business_json['business_id'] ] = business_json['stars']                    
                    #keep a set with all the related categories
                    categories = set(bjc).union(categories)-set([r])
                    #create a map storing the list of the restaurants in each related category
                    for cat in bjc:
                        if cat == r:
                            continue
                        if cat in catID2restID:
                            catID2restID[cat].append(business_json['business_id'])
                        else:
                            catID2restID[cat] = [business_json['business_id']]

    #save the restaurant ratings to disk and clear memory
    #print "output restaurant ratings"
    #with open ( path2sampledOutput + 'restaurantIds2ratings.txt', 'w') as f:
    #    for key in rest2rate:
    #        f.write( key + " " + str(rest2rate[key]) + "\n")
    rest2rate.clear()

    #store the hashtable category-to-restaurant_id in an intermediate result file for eventual future use (uncomment if needed)
    # with open('data_catID2restID.pickle', 'wb') as f:
    #    pickle.dump(catID2restID,f)

    ratingFilter = ['all']
    #ratingFilter = ['positive', 'negative', 'all']
    for sample_number in range(3):
        print
        restID2filteredRevID, totalFilteredReviews = readFilteredReviews(restaurantIDs, ratingFilter[sample_number]);
        print 'total filtered {} reviews: {}'.format(ratingFilter[sample_number], totalFilteredReviews)
        
        print "filtering out categories with less than {} {} reviews".format(min_num_reviews_per_cat, ratingFilter[sample_number])
        nz_count = 0
        valid_cats = []
        for i, cat in enumerate(catID2restID):
            # summarize the total of reviews for each category
            cat_total_reviews = 0
            for restID in catID2restID[cat]:
                if restID in restID2filteredRevID:
                    cat_total_reviews = cat_total_reviews + len(restID2filteredRevID[restID])
            # only those categories with more than min_num_reviews_per_cat reviews are considered valid
            if cat_total_reviews > min_num_reviews_per_cat:
                nz_count = nz_count + 1
                valid_cats.append(cat)
        print 'total valid categories for {} reviews: {}'.format(ratingFilter[sample_number], len(valid_cats))
 
        print "sampling categories. Sample", sample_number
        sample_size = min( max_num_cuisines, len(valid_cats)) # This specifies how many cuisines you would like to save
        cat_sample = random.sample(valid_cats, sample_size)  # select from the list of valid cats
        
        # joining the Sampled_Categories with the Category-to-Restaurant tables
        # output an inverted index Restaurant-to-SampledCategory (for each Restaurant, a list of all the sampled categories it relates to)
        sample_restID2catID={}
        for catID in cat_sample:
            for restID in catID2restID[catID]:
                if restID in restID2filteredRevID:
                    if restID not in sample_restID2catID:
                        sample_restID2catID[restID] = []
                    sample_restID2catID[restID].append(catID)
        #restID2filteredRevID.clear()
        print 'total sampled restaurants for {} reviews: {}'.format(ratingFilter[sample_number], len(sample_restID2catID))
        
        # collect reviews fields 'text' and 'stars' (rating) for each category
        print "reading Text and Rating from {} reviews file...".format(ratingFilter[sample_number])
        sample_cat2filteredReviewText={}
        sample_cat2filteredReviewRating={}
        num_reviews = 0
        with open (path2reviews, 'r') as f:
            for line in f.readlines():
                review_json = json.loads(line)
                restID = review_json['business_id']      
                # if the restaurant is in the sample set
                if restID in sample_restID2catID:
                    # if the review meets theconditions of the filter
                    revID = review_json['review_id']
                    if revID in restID2filteredRevID[restID]:
                        # replicate this review fields for every category the restaurant applies to (outer join)
                        # NOTE: this gives more weight to those reviews of restaurants that fit a lot of categories, because each
                        # review is counted once for every category of the restaurant. I think is ok for a cuisine analysis,
                        # but it definately not ok for Topic analysis, to know what people are talking about, because for that
                        # I want to count each review only once. The current script will distor the topic analysis, making it 
                        # about what people in those general-audience restaurants talk about and ignoring what people in all the
                        # single-cuisine speciality restaurants talks about.
                        for rcat in sample_restID2catID[restID]:
                            num_reviews = num_reviews + 1
                            # Output:
                            # -> Category-to-Review, containing the reviews Text field, for each of the sampled categories (lots of space)
                            # -> Category-to-Rating, containing the reviews Stars field, for each of the sampled categories
                            if rcat in sample_cat2filteredReviewText:
                                sample_cat2filteredReviewText[rcat].append(review_json['text'])
                                sample_cat2filteredReviewRating[rcat].append(str(review_json['stars']))
                            else:
                                sample_cat2filteredReviewText[rcat] = [review_json['text']]
                                sample_cat2filteredReviewRating[rcat] = [str(review_json['stars'])]

        # prepare output directories
        if save_sample or save_categories:
            print 'writing to', path2sampledOutput
            # root data folder - never delete
            if not os.path.exists(path2sampledOutput):
                os.mkdir(path2sampledOutput)
            # data sub-folders - delete and re-create
            dirpath = "{}{}/".format(path2sampledOutput, ratingFilter[sample_number])
            if os.path.exists(dirpath):
                shutil.rmtree(dirpath)
            os.mkdir(dirpath)
            path2categories = dirpath + "categories/"

        # output sample of restaurant reviews
        if save_sample:  
            sample_size = min(max_num_reviews, num_reviews)
            rev_sample = random.sample(range(num_reviews), sample_size)
            sorted_rev_sample = sorted(rev_sample)
            print "sampling {} restaurant reviews".format(sample_size)          
            count = 0  # the actual number of reviews saved in the sample file
            max_bound = 0  # accumulator used to define the lower bound of an interval
            sample_filteredReviewReplicatedByCat_Text = []
            sample_filteredReviewReplicatedByCat_Rating = []
            
            # for each Category in the map Category-to-Review
            for cat in sample_cat2filteredReviewText:
                print cat  # output the list of n categories randomly selected from those that have a review count above the threshold
                # max_bound marks the uppr bound of the random numbers already used for previous categories
                # this acts as the lower bound of the random numbers that will be used to pick reviews from current category's list
                # new_max_bound is the upper bound of the interval, each of the randomly generated integers that fall
                # in the [upper_bound, new_upper_bound] interval will be applied to select a review from this category
                new_max_bound = max_bound + len(sample_cat2filteredReviewText[cat])
                # the iteration stops when the random numbers start to fall outside the range allocated
                # for the current category (proportional to its number of reviews)
                # or when the count of reviews saved to the sample reaches the desired size
                while count < sample_size and sorted_rev_sample[count] < new_max_bound:
                    sample_filteredReviewReplicatedByCat_Text.append( sample_cat2filteredReviewText[cat][ sorted_rev_sample[count] - max_bound ].replace("\n", " ").strip() )
                    sample_filteredReviewReplicatedByCat_Rating.append( sample_cat2filteredReviewRating[cat][ sorted_rev_sample[count] - max_bound ] )
                    count = count + 1
                max_bound = new_max_bound

            print "output map Category-to-ReviewText (randomly sampled reviews)"
            with open (dirpath + "review_text_sample.txt", 'w') as f:
                f.write('\n'.join(sample_filteredReviewReplicatedByCat_Text).encode('ascii','ignore') )
        
            print "output map Category-to-ReviewRating (randomly sampled reviews)"
            with open (dirpath + "review_ratings_sample.txt", 'w') as f:
                f.write('\n'.join(sample_filteredReviewReplicatedByCat_Rating).encode('ascii','ignore') )

            with open (dirpath + "{}.txt".format(sample_size), 'w') as f:
                f.write('\n'.encode('ascii','ignore') )


        if save_categories:
            print "output one file per category with all the Category-to-ReviewID map (randomly sampled categories)"
            os.mkdir(path2categories)
            for cat in sample_cat2filteredReviewText:
                with open (path2categories + cat.replace('/', '-').replace(" ", "_") + ".txt" , 'w') as f:
                    f.write(u'\n'.join(sample_cat2filteredReviewText[cat]).encode('utf-8').strip())


# -----------------------------------------------------------------------------------------------
def sim_matrix():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    K_clusters = 10
    vectorizer = TfidfVectorizer(max_df=0.5, max_features=10000,
                                     min_df=2, stop_words='english',
                                     use_idf=True)
    
    if not os.path.isdir(path2Allcategories):
        print "path to categories:", path2Allcategories
        print "you need to generate the cuisines files 'categories' folder first"
        return
    
    text = [] # text is A LIST, each element corresponds to one of the categories ramdomly selected in the sample
    # the content of ech element of the list is the concatenation of the text of all the reviews of one category
    # the equivalent of a 'document'
    c_names = []
    cat_list = glob.glob (path2Allcategories + "*")
    cat_size = len(cat_list)
    if cat_size < 1:
        print "you need to generate the cuisines files 'categories' folder first"
        return
    
    sample_size = min(max_num_cuisines, cat_size)  
    cat_sample = sorted( random.sample(range(cat_size), sample_size) )
    #print (cat_sample)
    count = 0
    for i, item in enumerate(cat_list):
        # item is the categ name
        if i == cat_sample[count]:   # if this is the next of the randomly selected sample of numbers
            li =  item.split('/')
            cuisine_name = li[-1]
            c_names.append(cuisine_name[:-4].replace("_"," "))
            with open ( item ) as f:   # read the reviews for a category
                text.append(f.read().replace("\n", " "))
            count = count + 1
        
        if count >= len(cat_sample):
            print "generating cuisine matrix with:", count, "cuisines"
            break

    if len(text) < 1:
        print "the 'categories' folder does not contain any cuisines. Run this program ussing the '--cuisine' option"
    t0 = time()
    print("Extracting features from the training dataset using a sparse vectorizer (sklearn)")
    # Tokenize all the words from the corpus passed, and assign each word an index (column in X)
    # the list 'text' is the corpus, or collection of documents (each category is a 'document')
    # X is the training set matrix, with one row for each category and one column for each word
    # each element of the matrix X[i,j] is the normalized frequency of the term j in the document i
    # Note that the definition of vectorizer specifies the max_features value, also the min and max frequency filters and also IDF
    X = vectorizer.fit_transform(text)  # X is up to [30, 10000] (30 documents x 10000 terms)
    print("done in %fs" % (time() - t0))
    print("n_samples: %d, n_features: %d" % X.shape)

    t0 = time()
    print("Clustering features into topics using LDA (gensim models)")
    corpus = matutils.Sparse2Corpus(X,  documents_columns=False)
    lda = models.ldamodel.LdaModel(corpus, num_topics=100)    
    # LDA transforms the documents form their current space of 10000 diensions (terms) to a space lower dimensionality (100 'topics')
    # What it does is somehow clustering many columns into a single one, and outputs new representation of the documents as vectors in the new dimensional system.
    # Remember that each 'ducument' is a category (or 'cuisine' for us)
    # Rather than outputing the documents as a simple vector (an array of numbers in the new dimansional space) 
    # the output represents each document (cuisine) as a table of 100 rows (number of 'topics') and each row has 2 coulumns:
    # the topic-id and the weight of the topic for this particular document (cuisine) 
    # each row has one word and the weight of the word, but this can also be seen as the vectorial representation of the document in the new dimensional space,
    # or even more pedantically, as the probablity distribution on teh document in the form of 2-tuples (topic_id, p-value)
    # Note that topics don't have name, they are latent factors in the text and cannot be named automatically, 
    # only a human can assign them name if they are semantically homogeneous, but we are not concern with that here.
    # we don't care what the topics are called, we are just going to calculate the cosine distance 
    # between these cusines (aka documents, vectors, probability distributions)
    
    # Task 2: note that, by default this script is building the matrix with the foloowing Improvements:
    #  - grouping all reviews from a category in a single document
    #  - IDF
    #  - LDA (without it, the matrix would take forever to compute) 
    doc_topics = lda.get_document_topics(corpus)
    print("done in %fs" % (time() - t0))

    t0 = time()
    cuisine_matrix = [] #similarity of topics
    print 'computing cosine similarity matrix'
    for i, doc_a in enumerate(doc_topics):
        print "category: %d : %s   -   n_topics: %d" % (i, c_names[i], len(doc_a))
        sim_vecs = []
        for j , doc_b in enumerate(doc_topics):
            w_sum = 0
            if ( i <= j ):
                norm_a = 0
                norm_b = 0
                
                for (my_topic_b, weight_b) in doc_b:
                    norm_b = norm_b + weight_b*weight_b

                for (my_topic_a, weight_a) in doc_a:
                    norm_a = norm_a + weight_a*weight_a
                    for (my_topic_b, weight_b) in doc_b:
                        if ( my_topic_a == my_topic_b ):
                            w_sum = w_sum + weight_a*weight_b

                norm_a = math.sqrt(norm_a)
                norm_b = math.sqrt(norm_b)
                denom = (float) (norm_a * norm_b)
                if denom < 0.0001:
                    w_sum = 0
                else:
                    w_sum = w_sum/(denom)  # cosine similarity
            else:
                w_sum = cuisine_matrix[j][i]  # copy symetric element (already calculated)
            sim_vecs.append(w_sum) # append element to the row

        cuisine_matrix.append(sim_vecs) # append row to the matrix

    print("done in %fs" % (time() - t0))


    # write the matrix to a file
    with open( path2Allcategories + 'cuisine_sim_matrix.csv', 'w') as f:
        for i_list in cuisine_matrix:
            s = ""
            my_max = max(i_list)
            for tt in i_list:
                s = s+str(tt/my_max) + " "  # string concatenation to form the line, dividing for the max in each line (is called augmented similarity)
            s = s.strip() # remove the last space after the last element of the line
            f.write(",".join(s.split())+"\n") #should the list be converted to m

    # print the names of the categories selected in the random sample
    # these are the names of each column and each row of the matrix
    with open(path2Allcategories + 'cuisine_indices.txt', 'w') as f:
        f.write( "\n".join(c_names))




# ---------------------------------------------------------------------------------
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='This program transforms the Yelp data and saves the cuisines in the category directory. It also samples reivews from Yelp. It can also generates a cuisine similarity matrix.')
    
    parser.add_argument('--cuisine', action='store_true',
                       help='Saves a sample (10) of the cuisines to the "categories" directory. For Task 2 and 3 you will experiment with individual cuisines. This option allows you to generate a folder that contains all of the cuisines in the Yelp dataset. You can run this multiple times to generate more samples or if your machine permits you can change a sample parameter in the code.')
    parser.add_argument('--sample', action='store_true',
                       help='Sample a subset of reviews from the yelp dataset which could be useful for Task 1. This will samples upto 100,000 restaurant reviews from 10 cuisines and saves the output in "review_sample_100000.txt", it also saves their corresponding raitings in the "review_ratings_100000.txt" file. You can run this multiple times to get several different samples.')
    parser.add_argument('--matrix', action='store_true',
                       help='Generates the cuisine similarity matrix which is used for Task 2. First we apply topic modeling to a sample (30) of the cuisines in the "categories" folder and measures the cosine similarity of two cuisines from their topic weights. This might take from half-an-hour to several hours time depending on your machine. The number of topics is 20 and the default number of features is 10000.')
    parser.add_argument('--all', action='store_true',
                       help='Does all of the above.')

    
    args = parser.parse_args()        
    if args.all or (args.sample and args.cuisine):
        print "saving sample and cuisine"
        main(True,True)
    elif args.sample:
        print "generating sample"
        main(args.sample, args.cuisine)
    elif args.cuisine:
        print "generating cuisine"
        main(args.sample, args.cuisine)

    if args.matrix or args.all:
        print "generating cuisine matrix"
        sim_matrix()
    #main()
