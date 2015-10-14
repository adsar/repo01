
# coding: utf-8

# #Predicting Hygiene Inspection Results
# 
# Data Mining Capstone - Task 6

# In[142]:

import graphlab


# #Read data
# 
# Loading reviews. 

# In[143]:

path2data = 'C:/as/Dropbox/files/DataMin/cap/data/t6/data/'
labeled_tot = 546
unlabeled_tot = 12753


# In[144]:

restaurant_features = graphlab.SFrame.read_csv(path2data+'hygiene.additional.csv')


# #Let's explore this data together
# 
# Data includes the restaurant attributes. 

# In[145]:

print len(restaurant_features)
print  labeled_tot, unlabeled_tot
restaurant_features.head(3)


# In[146]:

labels = graphlab.SFrame.read_csv('C:/as/Dropbox/files/DataMin/cap/data/t6/data/hygiene.labels.csv', header=True, column_type_hints=str)
restaurant_features.add_column(labels['label'],'label')
restaurant_features.head(2)


# In[147]:

reviews = graphlab.SFrame.read_csv('C:/as/Dropbox/files/DataMin/cap/data/t6/data/hygiene.csv', 
                                                         delimiter='', header=True, error_bad_lines=False, comment_char='', 
                                                         escape_char='\\', double_quote=False, quote_char='', 
                                                         skip_initial_space=True, column_type_hints=str)
restaurant_features.add_column(reviews['review'],'review')
restaurant_features.head(2)


# #Build the word count vector for each review

# In[148]:

restaurant_features['word_freq'] = graphlab.text_analytics.count_words(restaurant_features['review'])
restaurant_features.head(3)


# In[149]:

graphlab.canvas.set_target('ipynb')


# In[150]:

restaurant_features['zipcode'].show(view='Categorical')


# In[151]:

restaurant_features['rating'].show()


# #Build a classifier

# In[152]:

labeled_subset = restaurant_features[restaurant_features['label'] != '[None]']
train_data, test_data = labeled_subset.random_split(.8, seed=0)
test_data['label'].show(view='Categorical')


# In[153]:

labeled_subset['rating'].show()


# In[154]:

logistic_model = graphlab.logistic_classifier.create(train_data, 
                                                     target='label', 
                                                     features=['word_freq'], 
                                                     validation_set=test_data)


# examine the weights the learned classifier assigned to the features

# In[155]:

coefs = logistic_model['coefficients']


# In[156]:

coefs_list = sorted(coefs, key=lambda c: c['value'], reverse=True) # sorting an SFrame with sorted() converts to list


# In[157]:

coefs = coefs.sort('value', ascending=False)


# In[158]:

coefs.head()


# In[159]:

coefs.tail()


# 3. Assess the quality of the model

# In[160]:

logistic_model.evaluate(test_data, metric='roc_curve')


# In[163]:

logistic_model.show(view='Evaluation')


# In[164]:

unlabeled_subset = restaurant_features[restaurant_features['label'] == '[None]']


# In[165]:

predicted_labels = logistic_model.predict(unlabeled_subset)


# In[166]:

unlabeled_subset.add_column(predicted_labels, 'predicted')


# In[167]:

predicted_classes = logistic_model.classify(unlabeled_subset)


# In[168]:

predicted_classes.head()


# In[169]:

unlabeled_subset.add_column(predicted_classes['probability'], 'probability')


# In[184]:

def bal_pred(l, p):
    if p >= 0.99999999999:
        return str(int(l))
    else:
        return '0'

unlabeled_subset['balanced_prediction'] = map(lambda x: bal_pred(x['predicted'], x['probability']), unlabeled_subset)
unlabeled_subset.head()


# In[185]:

unlabeled_subset['balanced_prediction'].show(view='Categorical')


# In[186]:

out1= ['adsar001']
out1.extend(labeled_subset['label'])
print out1[0:10]
out1.extend(unlabeled_subset['balanced_prediction'])
print out1[len(labeled_subset['label'])-5 :len(labeled_subset['label'])+5]


# In[187]:

restaurant_features.add_column(graphlab.SArray(out1[1:]), 'adsar001')
restaurant_features['adsar001'].show(view='Categorical')


# In[188]:

unlab_out1= ['adsar001']
unlab_out1.extend(unlabeled_subset['balanced_prediction'])
print unlab_out1[0:10]
with open(path2data+'unlabset.pred', "wb+") as fo:
    fo.write("\r\n".join(unlab_out1))


# In[ ]:



