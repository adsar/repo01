
# coding: utf-8

# #Document retrieval from wikipedia data
# 
# #Infromation Retrieval: Similarity & Clustering

# In[1]:

p = 'Elton John'
p1 = 'Paul McCartney'
p2='Victoria Beckham'


# In[2]:

import graphlab


# #Load some text data - from wikipedia, pages on people

# In[3]:

people = graphlab.SFrame('people_wiki.gl/')


# Data contains:  link to wikipedia article, name of person, text of article.

# In[5]:

len(people)


# #Explore the dataset and checkout the text it contains
# 
# ##Exploring the entry for a person

# In[6]:

person = people[people['name'] == p]


# In[7]:

person


# #Get the word counts for person article

# In[28]:

person['word_count'] = graphlab.text_analytics.count_words(person['text'])


# In[29]:

print person['word_count']


# ##Sort the word counts for the person article

# ###Turning dictonary of word counts into a table

# In[30]:

person_word_count_table = person[['word_count']].stack('word_count', new_column_name = ['word','count'])


# ###Sorting the word counts to show most common words at the top

# In[32]:

person_word_count_table.sort('count',ascending=False)


# Most common words include uninformative words like "the", "in", "and",...

# #Compute TF-IDF for the corpus 
# 
# To give more weight to informative words, we weigh them by their TF-IDF scores.

# ##1 - Examine the TF-IDF for a person's article

# In[17]:

person = people[people['name'] == p]


# In[18]:

person[['tfidf']].stack('tfidf',new_column_name=['word','tfidf']).sort('tfidf',ascending=False)


# Words with highest TF-IDF are much more informative.

# # 2 - Manually compute distances between different people
# 
# Let's manually compare the distances between the articles for a few famous people.  

# In[19]:

person1 = people[people['name'] == p1]


# In[20]:

person2 = people[people['name'] == p2]


# ##Is person p closer to p1 than to p2?
# 
# We will use cosine distance, which is given by
# 
# (1-cosine_similarity) 
# 

# In[21]:

graphlab.distances.cosine(person['tfidf'][0],person1['tfidf'][0])


# In[22]:

graphlab.distances.cosine(person['tfidf'][0],person2['tfidf'][0])


# 
# #3 - Build a nearest neighbor model for document retrieval
# 
# We now create a nearest-neighbors model and apply it to document retrieval.  


# In[25]:

knn_model = graphlab.nearest_neighbors.create(people,features=['tfidf'],label='name')


# #Applying the nearest-neighbors model for retrieval

# ##Who is closest to person p?

# In[26]:

knn_model.query(person)


# In[27]:

knn_model.query(person2)


