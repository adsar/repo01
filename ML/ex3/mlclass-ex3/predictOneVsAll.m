function p = predictOneVsAll(all_theta, X)
%PREDICT Predict the label for a trained one-vs-all classifier. The labels 
%are in the range 1..K, where K = size(all_theta, 1). 
%  p = PREDICTONEVSALL(all_theta, X) will return a vector of predictions
%  for each example in the matrix X. Note that X contains the examples in
%  rows. all_theta is a matrix where the i-th row is a trained logistic
%  regression theta vector for the i-th class. You should set p to a vector
%  of values from 1..K (e.g., p = [1; 3; 1; 2] predicts classes 1, 3, 1, 2
%  for 4 examples) 

m = size(X, 1);
num_labels = size(all_theta, 1);

% You need to return the following variables correctly 
p = zeros(size(X, 1), 1);

% Add ones to the X data matrix
X = [ones(m, 1) X];

% ====================== YOUR CODE HERE ======================
% Instructions: Complete the following code to make predictions using
%               your learned logistic regression parameters (one-vs-all).
%               You should set p to a vector of predictions (from 1 to
%               num_labels).
%
% Hint: This code can be done all vectorized using the max function.
%       In particular, the max function can also return the index of the 
%       max element, for more information see 'help max'. If your examples 
%       are in rows, then, you can use max(A, [], 2) to obtain the max 
%       for each row.
%       

% theta' has 10 columns, one for each category, to the vectorized product
% of X * all_theta' is a matrix of 10 columns, each column j is the prob.
% of the examples being of the j category.
PROB = X * all_theta';

% If called with one input and two output arguments, `max' also
% returns the first index of the maximum value(s).
% p is a vertical vector where each i element is index to the max
% probability in each row, this index is a number from 1 to 10
% and it is also the predicted category

% max of matrix PROB, returning a vector, according to dimension 2
% (aka max of each row)
[maxProb, p] = max(PROB, [], 2);

% =========================================================================

% For handwriting recognition, this functino is called with a training set
% of 5,000 rows and 400 features. The features are the pixelz in a 20x20
% bitmap. The rows are 5,000 examples of hand-written digits. The 10
% categories are the 10 digits 1, 2, 3, .., 9, 0

end
