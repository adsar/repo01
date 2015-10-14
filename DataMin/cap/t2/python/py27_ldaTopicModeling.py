import logging
import glob
import argparse
from gensim import models
from gensim import matutils
from sklearn.feature_extraction.text import TfidfVectorizer
from time import time
from nltk.tokenize import sent_tokenize


def main(K, numfeatures, inputdir, num_display_words, outputdir):
    K_clusters = K
    vectorizer = TfidfVectorizer(max_df=0.5, max_features=numfeatures,
                                     min_df=2, stop_words='english',
                                     use_idf=True)
    ratingFilter = ['all', 'positive', 'negative']
    for sample_number in range(3):
		inputfile = "{}/{}/review_text_sample.txt".format(inputdir, ratingFilter[sample_number])
		print "\nProcessing Sample {}  -- reading {}".format(sample_number, inputfile)
		text = []
		output_text = []
		with open (inputfile, 'r') as f:
		    text = f.readlines()

		t0 = time()
		print("Extracting features from the training dataset using a sparse vectorizer")
		X = vectorizer.fit_transform(text)
		print("done in %fs" % (time() - t0))
		print("n_samples: %d, n_features: %d" % X.shape)
		
		# mapping from feature id to actual word
		id2words ={}
		for i,word in enumerate(vectorizer.get_feature_names()):
		    id2words[i] = word

		t0 = time()
		print("Applying topic modeling, using LDA")
		print(str(K_clusters) + " topics")
		corpus = matutils.Sparse2Corpus(X,  documents_columns=False)
		lda = models.ldamodel.LdaModel(corpus, num_topics=K_clusters, id2word=id2words)
		print("done in %fs" % (time() - t0))
		output_text.append("name,weight")
		for i, item in enumerate(lda.show_topics(num_topics=K_clusters, num_words=num_display_words, formatted=False)):
		    output_text.append("Topic," + str(i))
		    for weight,term in item:
		        output_text.append( term + "," + str(weight) )

		outputfile = "{}/{}/sample_topics.txt".format(outputdir, ratingFilter[sample_number])
		print "writing topics to file:", outputfile
		with open ( outputfile, 'w' ) as f:
		    f.write('\n'.join(output_text))
        
        
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='This program takes in a file and some parameters and generates topic modeling from the file. This program assumes the file is a line corpus, e.g. list or reviews and outputs the topic with words and weights on the console.')
    
    parser.add_argument('-i', dest='inputdir', default=".", 
                       help='Specifies the file which is used by to extract the topics. The program assumes that there are 5 subfolders containing samples, names 1..5. The name of the input file is "review_text_sample.txt"')
    
    parser.add_argument('-o', dest='outputdir', default=".", 
                       help='Specifies the root output dir for the topics. The format of the data inside the output files is as a topic number followed by a list of words with corresdponding weights of the words. The program assumes that there are 5 subfolders containing samples, names 1..5. The default output file is "sample_topics.txt"')
    
    parser.add_argument('-K', default=100, type=int,
                       help='K is the number of topics to use when running the LDA algorithm. Default 100.')
    parser.add_argument('-featureNum', default=50000, type=int,
                       help='feature is the number of features to keep when mapping the bag-of-words to tf-idf vectors, (eg. lenght of vectors). Default featureNum=50000')
    parser.add_argument('-displayWN', default=15,type=int,
                       help='This option specifies how many words to display for each topic. Default is 15 words for each topic.')
    parser.add_argument('--logging', action='store_true',
                       help='This option allows for logging of progress.')
    
    
    args = parser.parse_args()
    #print args
    if args.logging:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    print "\nprocessing samples from root dir:", args.inputdir
    main(args.K, args.featureNum, args.inputdir, args.displayWN, args.outputdir)
    
