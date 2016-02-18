
# coding: utf-8

# In[100]:

import numpy as np
import pandas as pd
import sklearn
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier


# Load train and test data from /media/sf_as/Dropbox/files/DSScale/AnaMet/titanic

# In[101]:

path2files = "/media/sf_as/Dropbox/files/DSScale/AnaMet/titanic/"
train = pd.read_csv(path2files + "train.csv")
test = pd.read_csv(path2files + "test.csv")


# In[102]:

train.head(2)


# In[103]:

test.head(2)


# ## Data manipulation and Feature selection

# In[104]:

print len(test)


# In[105]:

train.columns[[2,4,5,6,7,9,10,11,1]]


# In[106]:

train[train.columns[[2,4,5,6,7,9,10,11,1]]].head(2)


# In[107]:

train[['Sex', 'Pclass', 'Age', "SibSp", "Parch", "Fare", 'Cabin', 'Embarked', 'Survived']].head(2)


# In[108]:

train[['Sex', 'Pclass', 'Age', "SibSp", "Parch", "Fare", 'Cabin', 'Embarked']].head(2)


# In[109]:

# preliminary selection of features
features_df = train[['Sex', 'Pclass', 'Age', "SibSp", "Parch", "Fare", 'Cabin', 'Embarked', 'Survived']].copy()
#features_df['Sex'] = features_df['Sex'] == 'female'
features_df = features_df.dropna()


# In[110]:

features_df.head(2)


# In[111]:

## Function to map the values of a categorical feature to a numerical range
## scikit-learn uses numpy and expects all the features to be numerical
def transform_feature( df, column_name ):
    unique_values = set( df[column_name].tolist() )
    transformer_dict = {}
    for ii, value in enumerate(unique_values):
        transformer_dict[value] = ii

    def label_map(y):
        return transformer_dict[y]
    df[column_name] = df[column_name].apply( label_map )
    return df


# In[112]:

### list of column names indicating which columns to transform; 
names_of_columns_to_transform = ['Sex', "Embarked"]
for column in names_of_columns_to_transform:
    features_df = transform_feature( features_df, column )
    
print( features_df.head() )
    
### Dataframe sintax to remove columns we cant make use of
features_df.drop("Cabin", axis=1, inplace=True)

print(features_df.columns.values)


# ### Repeat feature selection on the Test Set

# In[113]:

test_features_df = test[['Sex', 'Pclass', 'Age', "SibSp", "Parch", "Fare", 'Embarked']].copy()
test_features_df['Age'].fillna(0, inplace=True)
test_features_df['Fare'].fillna(0, inplace=True)
test_features_df[pd.isnull(test_features_df).any(axis=1)]


# In[114]:

fare_avg = test_features_df.groupby(['Pclass'])['Fare'].mean()
fare_avg.head()


# In[115]:

### list of column names indicating which columns to transform; 
names_of_columns_to_transform = ['Sex', "Embarked"]
for column in names_of_columns_to_transform:
    test_features_df = transform_feature( test_features_df, column )
    
print( test_features_df.head() )


# ## Model-Training, Scoring and Prediction

# In[116]:

predictors = ['Sex', 'Pclass', 'Age', "SibSp", "Parch", "Fare", 'Embarked']


# ### Random Forest Classifier

# In[117]:

# Initialize our algorithm with the default paramters
# n_estimators is the number of trees we want to make
# min_samples_split is the minimum number of rows we need to make a split
# min_samples_leaf is the minimum number of samples we can have at the place where a tree branch ends (the bottom points of the tree)
rf = RandomForestClassifier(random_state=1, n_estimators=10, min_samples_split=2, min_samples_leaf=1)
# Compute the accuracy score for all the cross validation folds.  (much simpler than what we did before!)
scores = cross_validation.cross_val_score(rf, features_df[predictors], features_df["Survived"], cv=3)

# Take the mean of the scores (because we have one for each fold)
print(scores.mean())


# In[118]:

## Train model (fit params)
rf.fit(features_df[predictors], features_df['Survived'])


# In[119]:

## Prediction
rf_predicted_y = rf.predict(test_features_df[predictors])
# look at results
test_data = test_features_df[predictors]
test_data['rf_predicted_y'] = rf_predicted_y
test_data.head()


# ### Logistic regression model

# In[120]:

### Training and Accuracy Scoring
import sklearn.linear_model as lm
lr = lm.LogisticRegression()
lr.fit(features_df[predictors], features_df['Survived'])
## compute the scores (a different sintax)
cross_validation.cross_val_score(lr, features_df[predictors], features_df['Survived'])


# In[121]:

### Prediction
lr_predicted_y = lr.predict(test_features_df[predictors])
# look at results
test_data['lr_predicted_y'] = rf_predicted_y
test_data.head()


# In[122]:

result_df = pd.DataFrame()
result_df['PassengerId'] = test['PassengerId']
result_df['Survived'] = test_data['lr_predicted_y']
result_df.to_csv(path2files + "logreg01.csv", columns=['PassengerId','Survived'], header=True,mode = 'w', index=False)


# In[123]:

result_df.head()


# In[124]:

# Estimate the score after imputation of the missing values
X_missing = test_features_df[predictors].copy()

from sklearn.preprocessing import Imputer
imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
imp.fit(features_df[predictors])
imp.transform(X_missing)


# In[125]:

X_missing.head()


# In[126]:

## Prediction
rf2_predicted_y = rf.predict(X_missing)
# look at results
test_data = X_missing.copy()
test_data['rf2_predicted_y'] = rf2_predicted_y.copy()
test_data.head()


# In[127]:

rf2_result_df = pd.DataFrame()
rf2_result_df['PassengerId'] = test['PassengerId'].copy()
rf2_result_df['Survived'] = test_data['rf2_predicted_y']
rf2_result_df.to_csv(path2files + "ranfor01.csv", columns=['PassengerId','Survived'], header=True,mode = 'w', index=False)


# In[ ]:



