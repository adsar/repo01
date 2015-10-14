function [theta, J_history] = gradientDescentMulti(X, y, theta, alpha, num_iters)
%GRADIENTDESCENTMULTI Performs gradient descent to learn theta
%   theta = GRADIENTDESCENTMULTI(x, y, theta, alpha, num_iters) updates theta by
%   taking num_iters gradient steps with learning rate alpha

% Initialize some useful values
m = length(y); % number of training examples
J_history = zeros(num_iters, 1);

for iter = 1:num_iters

    % ====================== YOUR CODE HERE ======================
    % Instructions: Perform a single gradient step on the parameter
    %               vector theta.
    %
    % NOTE: Because the code below is properly vectorized, it will
    %       support any number of features
    %
    % Hint: While debugging, it can be useful to print out the values
    %       of the cost function (computeCostMulti) and gradient here.
    %
    %   h is a [m,1] vector with the value of the hypothesis function
    %       for every value of the row X(i)
    h = X * theta;

    %   sumation: multiplying X'(transposed) by the vector (h - y)
    %       calculates the summation of each feature value X(i,j)
    %       multiplied by (hi - yi) for each data point (row i),
    %       all in one single vector operation
    S =  X' * (h - y) / m;

    theta = theta - alpha * S;

    % ============================================================

    % Save the cost J in every iteration    
    J_history(iter) = computeCostMulti(X, y, theta);

end

end
