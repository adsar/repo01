
# coding: utf-8

# #Building a song recommender
# 
# 
# #Fire up GraphLab Create

# In[8]:

import graphlab


# #Load music data

# In[9]:

song_data = graphlab.SFrame('song_data.gl/')


# #Explore data
# 
# Music data shows how many times a user listened to a song, as well as the details of the song.

# In[10]:

song_data.head()


# ##Showing the most popular songs in the dataset

# In[11]:

graphlab.canvas.set_target('ipynb')


# In[12]:

song_data['song'].show()


# In[13]:

len(song_data)


# ##Count number of unique users in the dataset

# In[14]:

users = song_data['user_id'].unique()


# In[15]:

len(users)


# #Create a song recommender

# In[ ]:

train_data,test_data = song_data.random_split(.8,seed=0)


# ##Simple popularity-based recommender

# In[ ]:

popularity_model = graphlab.popularity_recommender.create(train_data,
                                                         user_id='user_id',
                                                         item_id='song')


# ###Use the popularity model to make some predictions
# 
# A popularity model makes the same prediction for all users, so provides no personalization.

# In[ ]:

popularity_model.recommend(users=[users[0]])


# In[ ]:

popularity_model.recommend(users=[users[1]])


# ##Build a song recommender with personalization
# 
# We now create a model that allows us to make personalized recommendations to each user. 

# In[ ]:

personalized_model = graphlab.item_similarity_recommender.create(train_data,
                                                                user_id='user_id',
                                                                item_id='song')


# ###Applying the personalized model to make song recommendations
# 
# As you can see, different users get different recommendations now.

# In[ ]:

personalized_model.recommend(users=[users[0]])


# In[ ]:

personalized_model.recommend(users=[users[1]])


# ###We can also apply the model to find similar songs to any song in the dataset

# In[ ]:

personalized_model.get_similar_items(['With Or Without You - U2'])


# In[ ]:

personalized_model.get_similar_items(['Chan Chan (Live) - Buena Vista Social Club'])


# #Quantitative comparison between the models
# 
# We now formally compare the popularity and the personalized models using precision-recall curves. 

# In[ ]:

if graphlab.version[:3] >= "1.6":
    model_performance = graphlab.compare(test_data, [popularity_model, personalized_model], user_sample=0.05)
    graphlab.show_comparison(model_performance,[popularity_model, personalized_model])
else:
    get_ipython().magic(u'matplotlib inline')
    model_performance = graphlab.recommender.util.compare_models(test_data, [popularity_model, personalized_model], user_sample=.05)


# The curve shows that the personalized model provides much better performance. 

# ## Assignment

# 1 -  Counting Unique Users

# In[23]:

def uniqueUsers(artist):
    songs = song_data[song_data['artist'] == artist]
    print 'user-song occurrences: ' + str(len(songs))
    unique_users = songs['user_id'].unique()
    print artist +"'s unique users: " + str(len(unique_users))


# In[25]:

uniqueUsers('Kanye West')
uniqueUsers('Foo Fighters')
uniqueUsers('Taylor Swift')
uniqueUsers('Lady GaGa')


# 2 - Using groupby-aggregate to find the most popular and least popular artist

# In[65]:

def popularityRank():
    play_count = song_data.groupby(key_columns='artist',
                                    operations={'total_count': graphlab.aggregate.SUM('listen_count')})
    l = len(play_count) 
    print l
    splay_count = play_count.sort(['total_count', 'artist'], ascending=False)
    print splay_count[0]
    print splay_count[l-1]


# In[66]:

popularityRank()


# 3 - Using groupby-aggregate to find the most recommended songs

# In[76]:

train_data,test_data = song_data.random_split(.8,seed=0)


# In[77]:

personalized_model = graphlab.item_similarity_recommender.create(train_data,
                                                                user_id='user_id',
                                                                item_id='song')


# In[88]:

print len(test_data)


# In[80]:

unique_test_users = test_data['user_id'].unique()
print 'unique_test_users: ' + str(len(unique_test_users))


# In[82]:

subset_test_users = unique_test_users[0:10000]
subset_test_users.head()


# In[83]:

recommendations = personalized_model.recommend(subset_test_users,k=1)
recommendations.head()


# In[84]:

rec_count = recommendations.groupby(key_columns='song',
                                    operations={'count': graphlab.aggregate.COUNT()})
rec_count.head()


# In[94]:

print len(rec_count), rec_count['count'].sum()
srec_count = rec_count.sort('count', ascending=False)


# In[95]:

srec_count.head()


# In[96]:

srec_count.tail()


# In[ ]:



