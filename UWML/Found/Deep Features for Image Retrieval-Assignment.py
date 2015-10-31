
# coding: utf-8

# #Building an image retrieval system with deep features
# 
# 
# #Assignment

# In[4]:

import graphlab


# #Load the CIFAR-10 dataset
# 
# We will use a popular benchmark dataset in computer vision called CIFAR-10.  
# 
# (We've reduced the data to just 4 categories = {'cat','bird','automobile','dog'}.)
# 
# This dataset is already split into a training set and test set. In this simple retrieval example, there is no notion of "testing", so we will only use the training data.

# In[5]:

image_train = graphlab.SFrame('image_train_data/')


# #Computing deep features for our images
# 
# The two lines below allow us to compute deep features.  This computation takes a little while, so we have already computed them and saved the results as a column in the data you loaded. 
# 
# (Note that if you would like to compute such deep features and have a GPU on your machine, you should use the GPU enabled GraphLab Create, which will be significantly faster for this task.)

# In[ ]:

#deep_learning_model = graphlab.load_model('http://s3.amazonaws.com/GraphLab-Datasets/deeplearning/imagenet_model_iter45')
#image_train['deep_features'] = deep_learning_model.extract_features(image_train)


# In[5]:

image_train.head()


# #Train a nearest-neighbors model for retrieving images using deep features
# 
# We will now build a simple image retrieval system that finds the nearest neighbors for any image.

# In[6]:

knn_model = graphlab.nearest_neighbors.create(image_train,features=['deep_features'],
                                             label='id')


# #Use image retrieval model with deep features to find similar images
# 
# Let's find similar images to this cat picture.

# In[7]:

graphlab.canvas.set_target('ipynb')
cat = image_train[18:19]
cat['image'].show()


# In[8]:

knn_model.query(cat)


# We are going to create a simple function to view the nearest neighbors to save typing:

# In[9]:

def get_images_from_ids(query_result):
    return image_train.filter_by(query_result['reference_label'],'id')


# In[10]:

cat_neighbors = get_images_from_ids(knn_model.query(cat))


# In[11]:

cat_neighbors['image'].show()


# Very cool results showing similar cats.
# 
# ##Finding similar images to a car

# In[12]:

car = image_train[8:9]
car['image'].show()


# In[13]:

get_images_from_ids(knn_model.query(car))['image'].show()


# #Just for fun, let's create a lambda to find and show nearest neighbor images

# In[14]:

show_neighbors = lambda i: get_images_from_ids(knn_model.query(image_train[i:i+1]))['image'].show()


# In[15]:

show_neighbors(8)


# In[16]:

show_neighbors(26)


# # 1. Computing summary statistics of the data:
# Using the training data, compute the sketch summary of the ‘label’ column and interpret the results. 
# What’s the least common category in the training data?

# In[9]:

image_train['label'].sketch_summary()


# # 2. Creating category-specific image retrieval models
# create one model for each of the 4 image categories, {‘dog’,’cat’,’automobile’,bird’}

# In[10]:

image_train_dog = image_train[image_train['label']=='dog']
image_train_cat = image_train[image_train['label']=='cat']
image_train_automobile = image_train[image_train['label']=='automobile']
image_train_bird = image_train[image_train['label']=='bird']


# In[114]:

print len(image_train_dog), len(image_train_cat), len(image_train_automobile), len(image_train_bird)


# create a nearest neighbor model using the 'deep_features'

# In[12]:

knn_model_dog = graphlab.nearest_neighbors.create(image_train_dog,features=['deep_features'],
                                             label='id')


# In[13]:

knn_model_cat = graphlab.nearest_neighbors.create(image_train_cat,features=['deep_features'],
                                             label='id')


# In[14]:

knn_model_automobile = graphlab.nearest_neighbors.create(image_train_automobile,features=['deep_features'],
                                             label='id')


# In[15]:

knn_model_bird = graphlab.nearest_neighbors.create(image_train_bird,features=['deep_features'],
                                             label='id')


# In[16]:

image_test[0:1]


# In[17]:

image_test = graphlab.SFrame('image_test_data/')


# In[21]:

graphlab.canvas.set_target('ipynb')
image1 = image_test[0:1]
image1['image'].show()


# What is the nearest ‘cat’ labeled image in the training data to the cat image above?

# In[27]:

image1_cat_neighbors = knn_model_cat.query(image1)


# In[124]:

image1_cat_neighbors.head(1)


# In[116]:

neighbor_cats = image_train_cat.filter_by(image1_cat_neighbors.head(1)['reference_label'],'id')


# In[117]:

graphlab.canvas.set_target('ipynb')
neighbor_cats['image'].show()


# What is the nearest ‘dog’ labeled image in the training data to the cat image above

# In[39]:

image1_dog_neighbors = knn_model_dog.query(image1)


# In[40]:

image1_dog_neighbors.head(1)


# In[119]:

neighbor_dogs = image_train_dog.filter_by(image1_dog_neighbors.head(1)['reference_label'],'id')


# In[120]:

neighbor_dogs['image'].show()


# # 3. Nearest-neighbors classification

# compute the mean distance between image1 at its 5 nearest neighbors that were labeled ‘cat’ in the training data

# In[49]:

image1_cat_neighbors.head(5)['distance'].mean()


# compute the mean distance between image1 at its 5 nearest neighbors that were labeled ‘dog’ in the training data

# In[50]:

image1_dog_neighbors.head(5)['distance'].mean()


# image1 is closer to the nearest 5 cats than to the nearest 5 dogs, this is an example of the k-nearest neighbors classifier, where we use the label of neighboring points to predict the label of a test point.

# # 4. [Challenging Question] Computing nearest neighbors accuracy using SFrame operations

# A nearest neighbor classifier predicts the label of a point as the most common label of its nearest neighbors. In this question, we will measure the accuracy of a 1-nearest-neighbor classifier, i.e., predict the output as the label of the nearest neighbor in the training data.

# subsetting the test data by label:

# In[95]:

len( image_test)


# In[52]:

image_test_dog = image_test[image_test['label']=='dog']
image_test_cat = image_test[image_test['label']=='cat']
image_test_automobile = image_test[image_test['label']=='automobile']
image_test_bird = image_test[image_test['label']=='bird']


# In[96]:

len( image_test_bird)


# Retrieving the closes neighbour of a different label. We query with a whole set of items, and it will find the nearest neighbor of each item. 
# The output SFrame will contain a new column called ‘query_label’ which contains input index of the input item. 

# In[56]:

# First neighbor to the dog test images (image_test_dog) in the cat portion of the training data
dog_cat_neighbors = knn_model_cat.query(image_test_dog, k=1)


# In[57]:

dog_cat_neighbors.head(5)


# In[133]:

dog_dog_neighbors = knn_model_dog.query(image_test_dog, k=1)
dog_automobile_neighbors = knn_model_automobile.query(image_test_dog, k=1)
dog_bird_neighbors = knn_model_bird.query(image_test_dog, k=1)


# - create an SFrame called dog_distances with 4 columns: the distances from ‘dog’ test examples to the respective nearest neighbors in each class in the training data:

# In[134]:

dog_distances = graphlab.SFrame()
#dog_distances['id'] = dog_cat_neighbors['query_label']


# In[135]:

dog_distances['dog-dog'] = dog_dog_neighbors['distance']
dog_distances['dog-cat'] = dog_cat_neighbors['distance']
dog_distances['dog-automobile'] = dog_automobile_neighbors['distance']
dog_distances['dog-bird'] = dog_bird_neighbors['distance']


# In[136]:

dog_distances.print_rows(num_rows=20, num_columns=4)


# In[137]:

def is_dog_correct(row):
    if min(row.values()) == row['dog-dog']:
        return 1
    else:
        return 0


# In[138]:

dog_distances.apply(is_dog_correct)


# In[139]:

sum(dog_distances.apply(is_dog_correct))


# In[140]:

len(dog_distances)


# In[141]:

print 'Accuracy = ', 100 * float(sum(dog_distances.apply(is_dog_correct))) / len(dog_distances)


# In[ ]:



