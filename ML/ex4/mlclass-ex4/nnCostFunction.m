function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda)
%NNCOSTFUNCTION Implements the neural network cost function for a two layer
%neural network which performs classification
%   [J grad] = NNCOSTFUNCTON(nn_params, hidden_layer_size, num_labels, ...
%   X, y, lambda) computes the cost and gradient of the neural network. The
%   parameters for the neural network are "unrolled" into the vector
%   nn_params and need to be converted back into the weight matrices. 
% 
%   The returned parameter grad should be a "unrolled" vector of the
%   partial derivatives of the neural network.
%

% Reshape nn_params back into the parameters Theta1 and Theta2, the weight matrices
% for our 2 layer neural network
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

% Setup some useful variables
m = size(X, 1);
         
% You need to return the following variables correctly 
J = 0;
Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));


% ====================== YOUR CODE HERE ======================
% Instructions: You should complete the code by working through the
%               following parts.
%
% Part 1: Feedforward the neural network and return the cost in the
%         variable J. After implementing Part 1, you can verify that your
%         cost function computation is correct by verifying the cost
%         computed in ex4.m


for i = 1:m
    % forward propagation to calculate the hypothesis function
    a1 = X(i, :)';

    z2 = Theta1 * [1; a1];
    a2 = sigmoid(z2);

    z3 = Theta2 * [1; a2];
    a3 = sigmoid(z3);

    h_theta_Xi = a3;

    % reconstruct the training example output labels vector
    vyi = zeros(num_labels,1);
    vyi(y(i)) = 1;

    % calculate the cost function (devectorized for pedagogic clarity)
    costi = 0;
    for k = 1:num_labels
        deltak = -vyi(k) * log(h_theta_Xi(k)) - (1 - vyi(k)) * log(1 - h_theta_Xi(k));
        costi = costi + deltak;
    endfor

    J = J + costi;
endfor

J = J / m;

% regularization term
% Note that excludes 1st column, which are the constants (aka bias unit)
reg = (sum(sum(Theta1(:,2:end).^2)) + sum(sum(Theta2(:,2:end).^2))) * lambda / (2 * m);

J = J + reg;


%
% Part 2: Implement the backpropagation algorithm to compute the gradients
%         Theta1_grad and Theta2_grad. You should return the partial derivatives of
%         the cost function with respect to Theta1 and Theta2 in Theta1_grad and
%         Theta2_grad, respectively. After implementing Part 2, you can check
%         that your implementation is correct by running checkNNGradients
%
%         Note: The vector y passed into the function is a vector of labels
%               containing values from 1..K. You need to map this vector into a 
%               binary vector of 1's and 0's to be used with the neural network
%               cost function.
%
%         Hint: We recommend implementing backpropagation using a for-loop
%               over the training examples if you are implementing it for the 
%               first time.


% Using t as index of the training examples,
% calculate the sums of the gradients for all the training examples
for t = 1:m
% forward propagation to calculate the activation values
% input layer
    a1 = X(t, :)';

% hidden layer
    z2 = Theta1 * [1; a1];
    a2 = sigmoid(z2);

% output layer
    z3 = Theta2 * [1; a2];
    a3 = sigmoid(z3);

% reconstruct the training example output labels vector
    vy = zeros(num_labels,1);
    vy(y(t)) = 1;



% Back-Propagation to calculate the gradients

% output layer error vector
    delta3 = a3 - vy;
% Calculate the theta2 (hidden-layer-to-output-layer) gradient (skip the first row because it correspond to the constants)
theta2_grad_t = delta3 * [1; a2]';
% Accumulate the theta2 gradient for all traning examples
Theta2_grad = Theta2_grad + theta2_grad_t;

% hidden layer error vector
    delta2 = (Theta2' * delta3) .* [1; sigmoidGradient(z2)];
% Calculate the theta1 (input-layer-to-hidden-layer) gradient (skip the first row because it correspond to the constants)
    theta1_grad_t = delta2 * [1; a1]';
% Accumulate the theta1 gradient for all traning examples
    Theta1_grad = Theta1_grad + theta1_grad_t(2:end,:);

endfor

% average gradient over all training set

Theta1_grad  = Theta1_grad / m;
Theta2_grad  = Theta2_grad / m;





%
% Part 3: Implement regularization with the cost function and gradients.
%
%         Hint: You can implement this around the code for
%               backpropagation. That is, you can compute the gradients for
%               the regularization separately and then add them to Theta1_grad
%               and Theta2_grad from Part 2.
%

              Theta1_grad = Theta1_grad + [zeros(size(Theta1,1),1) Theta1(:,2:end)] * lambda / m;
              Theta2_grad = Theta2_grad + [zeros(size(Theta2,1),1) Theta2(:,2:end)] * lambda / m;
              

















% -------------------------------------------------------------

% =========================================================================

% Unroll gradients
grad = [Theta1_grad(:) ; Theta2_grad(:)];


end
