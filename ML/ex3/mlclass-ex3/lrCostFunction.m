function [J, grad] = lrCostFunction(theta, X, y, lambda)
%LRCOSTFUNCTION Compute cost and gradient for logistic regression with 
%regularization
%   J = LRCOSTFUNCTION(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta
%
% Hint: The computation of the cost function and gradients can be
%       efficiently vectorized. For example, consider the computation
%
%           sigmoid(X * theta)
%
%       Each row of the resulting matrix will contain the value of the
%       prediction for that example. You can make use of this to vectorize
%       the cost function and gradient computations. 
%
% Hint: When computing the gradient of the regularized cost function, 
%       there're many possible vectorized solutions, but one solution
%       looks like:
%           grad = (unregularized gradient for logistic regression)
%           temp = theta; 
%           temp(1) = 0;   % because we don't add anything for j = 0  
%           grad = grad + YOUR_CODE_HERE (using the temp variable)
%

% NOTE: (theta'*x) refers to a single training example (lower case x)
% x is a single row vector of dimension [1, n]
% (theta'*x) is an escalar
% The formula below is vectorized:
% z is a vector [m, 1] where z(i) = tetha' * x(i)

% Note that g = sigmoid(theta'x) is a vector [m, 1].
% g not the prediction, the actual prediction is a vector p[m, 1]
% where p(i) is 1 if g(i) >= 0.5
% p is not calculated in this function
                           
z = X * theta;
g = sigmoid(z);

                        
% Cost regularization term
m = size(X, 1);
r = lambda * sum(theta(2:end) .^2) / (2 * m);

% Regularized Logistic Regression cost function
cost = -y .* log(g) - (1 - y) .* log(1 - g);
J = sum(cost)/m + r;

% =============================================================
% Gradient Regularization Term; this is a vertical vector the size of theta,
% but the first element is zero because we do not regularize the bias element,
% theta(0).
% NOTE the ';' after the zero below, el ';' means row below
rg = lambda/m .* [0; theta(2:end)];
                        
% gradient of the cost is a vector (1, n)
% this formula looks like linear regression, just that
% in logistic regression we use the sigmoid function (g)

grad = grad(:);
grad = ((X' * (g - y)) / m) + rg ;

end
