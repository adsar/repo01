function [J, grad] = linearRegCostFunction(X, y, theta, lambda)
%LINEARREGCOSTFUNCTION Compute cost and gradient for regularized linear 
%regression with multiple variables
%   [J, grad] = LINEARREGCOSTFUNCTION(X, y, theta, lambda) computes the 
%   cost of using theta as the parameter for linear regression to fit the 
%   data points in X and y. Returns the cost in J and the gradient in grad

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost and gradient of regularized linear 
%               regression for a particular choice of theta.
%
%               You should set J to the cost and grad to the gradient.
%

% linear regression cost function
J = sum((X * theta - y).^2) / (2 * m);

% linear regresssion regularization (excluding bias term)
regTerm = lambda/(2 * m) * sum(theta(2:end).^2);

% regularized linear regression cost function
J = J + regTerm;


% linear regression cost function gradient
% this is a vector with one derivative for each feature j of theta


%   h is a [m,1] vector with the value of the hypothesis
%     for every value of the row X(i)
h = X * theta;

%   multiplying X'(transposed) by the error vector (h - y)
%   calculates the summation, over all the training examples,
%   of the product of each feature value X(i,j) by the error (hi - yi)
%   All the above in one single vector operation. X' has n rows, so
%   the result of multiplying by X' is a vertical vector of n rows,
%   just like the vector theta.
grad =  X' * (h - y) / m;

% regularized gradient (excluding the bias term)
grad = grad + lambda/m * [0; theta(2:end)];
% =========================================================================

grad = grad(:);

end
