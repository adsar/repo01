# this is a Work in Progress file, with the code 
# that automatically tries different methods in a loop

from sklearn.cross_validation import LeavePOut

classifier_map = dict()
classifier_map["Nearest Neighbors"]=KNeighborsClassifier(3)
classifier_map["Linear SVM"]=SVC(kernel="linear", C=0.025)
classifier_map["RBF SVM"]= SVC(gamma=2, C=1)
classifier_map["Decision Tree"]=DecisionTreeClassifier(max_depth=5)
classifier_map["Random Forest"]=RandomForestClassifier
    (max_depth=5, n_estimators=10, max_features=1)
classifier_map["AdaBoost"]=AdaBoostClassifier()
classifier_map["Naive Bayes"]=GaussianNB()
classifier_map["LDA"]=LDA()
classifier_map["QDA"]=QDA()

# build a term count
vectorizer = CountVectorizer(gmin_df=1)
corpus=["brown dog writing text", "the cow hat is brown"]
fit_corpus = vectorizer.fit_transform(corpus)
print(vectorizer.get_feature_names()[0:2])

# Build the feature and target label vectors
   data_target_tuples=[ ]
    for bp in behavioral_profiles:
        for pd in bp.product_descriptions:
            data_target_tuples.append((bp.type, pd.description))

    shuffle(data_target_tuples)

# Assemble the vectors
   X_data=[ ]
    y_target=[ ]
    for t in data_target_tuples:
        v = vectorizer.transform([t[1]]).toarray()[0]
        X_data.append(v)
        y_target.append(t[0])

    X_data=np.asarray(X_data)
    y_target=np.asarray(y_target)

# Start by using a Linear Support Vector Machine (SVM), which is a nice, heavy-hitter model 
# for sparse vector problems such as this one.
linear_svm_classifier = SVC(kernel="linear", C=0.025).

for key, value in classifier_map:

	# Cross-fold validation
	scores = cross_validation.cross_val_score(OneVsRestClassifier(linear_svm_classifier), X_data, y_target, cv=2)
	print("Accuracy using %s: %0.2f (+/- %0.2f) and %d folds" 
		% ("Linear SVM", scores.mean(), scores.std() * 2, 5))

# Train your behavioral profile model
    behavioral_profiler = SVC(kernel="linear", C=0.025)
    behavioral_profiler.fit(X_data, y_target)

# Playing with the model
print behavioral_profiler.predict(vectorizer.transform(['Some black Bauhaus shoes to go with your Joy Division hand bag']).toarray()[0])

#  Applying the trained model against our customers and their product descriptions
predicted_profiles=[ ]
ground_truth=[ ]
for c in customers:
    customer_prod_descs = ' '.join(p.description for p in 
c.product_descriptions)
    predicted =   behavioral_profiler.predict(vectorizer
.transform([customer_product_descriptions]).toarray()[0])
    predicted_profiles.append(predicted[0])
    ground_truth.append(c.type)
    print "Customer %d, known to be %s, was predicted to be %s" % (c.id,c.type,predicted[0])

# Computing your accuracy
 a=[x1==y1 for x1, y1 in zip(predicted_profiles,ground_truth)]
    accuracy=float(sum(a))/len(a)
    print "Percent Profiled Correctly %.2f" % accuracy
# The result should be 95 percent with the default profile data provided. If this were real data, that would be a reasonably good accuracy rate.

