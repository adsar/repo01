function [J, grad] = costFunction(theta, X, y)
%COSTFUNCTION Compute cost and gradient for logistic regression
%   J = COSTFUNCTION(theta, X, y) computes the cost of using theta as the
%   parameter for logistic regression and the gradient of the cost
%   w.r.t. to the parameters.

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
% Note: grad should have the same dimensions as theta
%

% NOTE: (theta'*x) refers to a single training example (lower case x)
% x is a single row vector of dimension [1, n]
% (theta'*x) is an escalar
% The formula below is vectorized:
% z is a vector [m, 1] where z(i) = tetha' * x(i)

z = X * theta;
g = sigmoid(z);

% Note that g = sigmoid(theta'x) is a vector [m, 1].
% g not the prediction, the actual prediction is a vector p[m, 1]
% where p(i) is 1 if g(i) >= 0.5
% p is not calculated in this function

% The formula to calculate the cost J is de-vectorized for
% clarity. If I vectorize it it looks very clean but it gives
% me no information about the dimensions of the operands,
% which become self-documented when de-vectorized
m = size(X, 1);
cost = zeros(m, 1);
for i = 1 : m
    cost(i) = -y(i) * log(g(i)) - (1 - y(i)) * log (1 - g(i));
endfor
J = sum(cost) / m;

% gradient of the cost is a vector (1, n)
% this formula looks like linear regression but
% in logistic regression we use the sigmoid function
n = size(X, 2);
grad = zeros(1, n);
for j = 1 : n
    grad(j) = sum((g - y) .* X(:,j)) / m;
endfor


% =============================================================

end

