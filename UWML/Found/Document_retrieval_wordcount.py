
# coding: utf-8

# #Document retrieval from wikipedia data
# 
# #Infromation Retrieval: Similarity & Clustering

# In[1]:

p = 'Elton John'
p1 = 'Paul McCartney'
p2='Victoria Beckham'
#%load filename.py

# In[2]:

import graphlab


# #Load some text data - from wikipedia, pages on people

# In[3]:

people = graphlab.SFrame('people_wiki.gl/')


# In[4]:

len(people)


# In[5]:

people['word_count'] = graphlab.text_analytics.count_words(people['text'])
people.head()


# In[6]:

person = people[people['name'] == p]


# In[7]:

person


# # 2 - Manually compute distances between different people


# In[8]:

person1 = people[people['name'] == p1]


# In[9]:

person2 = people[people['name'] == p2]


# ##Is person p closer to p1 than to p2?
# 
# We will use cosine distance, which is given by
# 
# (1-cosine_similarity) 
# 

# In[10]:

graphlab.distances.cosine(person['word_count'][0],person1['word_count'][0])


# In[11]:

graphlab.distances.cosine(person['word_count'][0],person2['word_count'][0])


# 
# #3 - Build a nearest neighbor model for document retrieval
# 
# We now create a nearest-neighbors model and apply it to document retrieval.  

# In[12]:

knn_model_wc = graphlab.nearest_neighbors.create(people,features=['word_count'],label='name', distance='cosine')


# #Applying the nearest-neighbors model for retrieval

# ##Who is closest to person p?

# In[13]:

knn_model_wc.query(person)


# In[14]:

knn_model_wc.query(person2)






