function p = predict(theta, X)
%PREDICT Predict whether the label is 0 or 1 using learned logistic 
%regression parameters theta
%   p = PREDICT(theta, X) computes the predictions for X using a 
%   threshold at 0.5 (i.e., if sigmoid(theta'*x) >= 0.5, predict 1)

m = size(X, 1); % Number of training examples

% You need to return the following variables correctly
p = zeros(m, 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Complete the following code to make predictions using
%               your learned logistic regression parameters. 
%               You should set p to a vector of 0's and 1's
%

% NOTE: (theta'*x) refers to a single training example,
% with lower case x, this x is a single row from the matrix X (which
% are vectors of dimension [1, n]). By convention,
% one-dimensional vectors x are arranged vertically, so they are
% of dimension [n, 1]

    for i = 1 : m
        x = X(i,:)';
        g = sigmoid(theta' * x);
        if g >= 0.5
            p(i) = 1;
        else
            p(i) = 0;
        endif
    endfor



% =========================================================================


end
