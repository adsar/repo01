function [J, grad] = costFunctionReg(theta, X, y, lambda)
%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
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

z = X * theta;
g = sigmoid(z);


% regularization term
n = size(X, 2);
theta_squared = theta(2:n)' * theta(2:n);
r = lambda * theta_squared / (2 * m);

m = size(X, 1);
cost = zeros(m, 1);
for i = 1 : m
    cost(i) = -y(i) * log(g(i)) - (1 - y(i)) * log (1 - g(i));
endfor
J = sum(cost) / m + r;



grad = zeros(1, n);
grad(1) = (sum((g - y) .* X(:,1)) / m);  % we do not regularize parameter theta 0
for j = 2 : n
    grad(j) = (sum((g - y) .* X(:,j)) / m) + lambda * theta(j) / m;
endfor


% =============================================================

end
