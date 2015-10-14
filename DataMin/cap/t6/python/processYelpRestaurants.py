import math
import json
import random
import logging
from time import time
import glob
import argparse
import os
import shutil
import string

from gensim import models
from gensim import matutils
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import numpy as np
from sklearn import cluster
from sklearn.preprocessing import StandardScaler
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

path2files="/mnt/hgfs/sh_dev/Hygiene/"
path2training=path2files+"hygiene.dat"
path2additional=path2files+"hygiene.dat.additional"
path2labels=path2files+"hygiene.dat.labels"

training_set_size = 546

# ----------------------------------------------------------------------------------------------
stopset = set(stopwords.words('english'))
stemmer = PorterStemmer()
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

# ----------------------------------------------------------------------------------------------
def cleanup_tokenize(text):
    if not text or len(text) == 0: return text
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if not w in stopset]
    tokens = filter(lambda x: x.isalpha(), tokens)
    tokens = [i for i in tokens if i not in string.punctuation]
    stems = stem_tokens(tokens, stemmer)
    return " ".join(stems)

######## 

# ----------------------------------------------------------------------------------------------
def main():
    training, training_label, test = read_dataset()

    doc_topics_idf_100 = create_bow_representation()

    select_optimum_classifier()

    predict()

# ----------------------------------------------------------------------------------------------
def read_dataset()
    # read the list of business
    print("reading restaurant reviews")
    training = []
       test = []
    line_counter = 0
    with open (path2training, 'r') as f:
        for line in f.readlines():
            line_counter += 1
            if counter <= training_set_size:
                training.append(cleanup_tokenize(line))
            else:
                test.append(cleanup_tokenize(line))

    print("reading training labels")
    training_label = []
    line_counter = 0
    with open (path2labels, 'r') as f:
        for line in f.readlines():
            line_counter += 1
            if counter > training_set_size:
            break
            training_label.append(int(line))

    return training, training_label, test

# ----------------------------------------------------------------------------------------------
def create_bow_representation():

    # create bow (bag of words) representations: 546 docs x 10000 features
    X_idf = get_tfidf_representation(training_set, True)

    # reduce dimensionality: 100 topics
    doc_topics_idf_100 = reduce_dimensionality_with_lda(X_idf, 100)
    
    print('LDA 100-topic output:')
    for i, doc_a in enumerate(doc_topics_idf_100 ):
        print("training example: %d  -   n_topics: %d" % (i, len(doc_a)))
        for (my_topic_a, weight_a) in doc_a:
            print("    -    topic id: %d  -  weight: %f" % (my_topic_a, weight_a))
    
    return doc_topics_idf_100

# ----------------------------------------------------------------------------------------------
def get_tfidf_representation(text, idf):
    t0 = time()
    print("Extracting features from the training dataset. IDF =", idf)
    print("Using a sparse vectorizer from scikit-learn")
    # Tokenizes all the words from the corpus passed, and assign each word an index (column in X)
    # the list 'text' is the corpus, or collection of documents (each category is a 'document')
    # X is the training set matrix, with one row for each category and one column for each word
    # each element of the matrix X[i,j] is the normalized frequency of the term j in the document i
    # Note that the definition of vectorizer specifies the max_features value, also the min and max frequency filters and also IDF
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    vectorizer = TfidfVectorizer(max_df=0.5, max_features=10000,
                                     min_df=2, stop_words='english',
                                     use_idf=idf)
    X = vectorizer.fit_transform(text)  
    # X is up to [546, 10000] (546 documents x 10000 terms)
    print("done in %fs" % (time() - t0))
    print("n_samples: %d, n_features: %d" % X.shape)
    return X

# ----------------------------------------------------------------------------------------------
def reduce_dimensionality_with_lda(X, n_top):
    # LDA transforms the documents form their current space of 10000 diensions (terms) to a space lower dimensionality (100 'topics')
    # What it does is somehow clustering many columns into a single one, and outputs new representation of the documents as vectors in the new dimensional system.
    # the output represents each document (restaurant) as a table of 100 rows (number of 'topics') and each row has 2 coulumns:
    # the topic-id and the weight of the topic for this particular document (restaurant) 
    # this can also be seen as the vectorial representation of the document in the new dimensional space,
    # or as the probablity distribution on the document in the form of 2-tuples (topic_id, p-value)
    # Note that topics don't have name, they are latent factors in the text and cannot be named automatically, 
    # only a human can assign them name if they are semantically homogeneous, but we are not concern with that here.
    # we don't care what the topics are called, we are just going to calculate the cosine distance 
    # between these restauants (aka training examples, documents, bows, vectors, probability distributions)

    t0 = time()
    print("Dimensionality reduction applying a topic model, num topics:", n_top)
    print("Using LDA (gensim models)")
    corpus = matutils.Sparse2Corpus(X,  documents_columns=False)
    lda = models.ldamodel.LdaModel(corpus, num_topics=n_top)
    doc_topics = lda.get_document_topics(corpus)
    print("done in %fs" % (time() - t0))
    return doc_topics

# ----------------------------------------------------------------------------------------------
def select_optimum_classifier():
    # trying different methods
    doc_topics_idf_100_class_01 = train_classifier(doc_topics_idf_100, training_label, "LogisticRegression")
    predicted_labels = predict_labels(doc_topics_idf_100_kmeans_10, test_set)

    # save the names of the categories selected in the random sample
    # these are the names of each column and each row of the matrix
    with open(path2matrix + '"prediction_classifier_01.txt', 'w') as f:
        f.write( "\n".join(predicted_labels))

# ----------------------------------------------------------------------------------------------
def train_classifier(training, training_label, method):
    print("Training classifier with {}".format(method))
    # normalize dataset for easier parameter selection
    X = StandardScaler().fit_transform(training)
    y_pred = ''
    return y_pred

# ----------------------------------------------------------------------------------------------
def save_predicted_labels(predicted_labels, filename):
    with open(path2files + filename, 'w') as f:
        labels = ["%d" % label for label in predicted_labels]
        f.write( "\n".join(labels))

# ---------------------------------------------------------------------------------
if __name__=="__main__":
main()

