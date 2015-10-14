function p = predict(Theta1, Theta2, X)
%PREDICT Predict the label of an input given a trained neural network
%   p = PREDICT(Theta1, Theta2, X) outputs the predicted label of X given the
%   trained weights of a neural network (Theta1, Theta2)

% Useful values
m = size(X, 1);
num_labels = size(Theta2, 1);

% You need to return the following variables correctly 
p = zeros(size(X, 1), 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Complete the following code to make predictions using
%               your learned neural network. You should set p to a 
%               vector containing labels between 1 to num_labels.
%
% Hint: The max function might come in useful. In particular, the max
%       function can also return the index of the max element, for more
%       information see 'help max'. If your examples are in rows, then, you
%       can use max(A, [], 2) to obtain the max for each row.
%

% X is a matrix of 5,000 rows with 400 columns, each row
% represents a bitmap of 20x20. We have to recognize what
% hand-written digit is represented in each row, and return
% the 5,000 digits represented in the input matrix X.

% theta1 and theta 2 are given to us, we just have to apply them
% to X and return a prediction.


% theta1: computes the input to layer 2 from the input to layer 1.
% in other words, layer1 process is, essentially,
% a vector multiplication by theta1  (actually the sigmoid of that.)
% Looking at theta1 as a process:
% - The input to theta1 is a vertical X vector of 400 units or
%   features, dimension [400,1]. This is the training example, 400 pixels
%   from a 20x20 bitmap. In order to feed the X data to layer 1, we
%   need to go over the X matrix row by row with a for loop and
%   also we need to add the constant factor
%   and transpose the row so it arranges vertically.
% - The output from theta1 is 25 columns, which is the input
%   to layer2 (layer2 has 25 units or features)
% So theta1 must have dimension [25, 401] (400 + 1 for the bias element)

for i = 1 : m
    z1 = Theta1 * [1 X(i,:)]';
    output_layer1 = sigmoid(z1);  % a1

% theta2: computes the input to layer3 from the input to layer 2.
% Looking at theta2 as a process:
% - The input to theta2 is a vertical a1 vector of 25 units or
%   features (columns).
% - The output from theta2 is 10 columns, which is the input
%   to layer3
% Layer3 has 10 units or features, one for each of the categories
% that we are classifying the examples into (the 10 digits.)
% So theta2 must have dimension [10, 26]
% note the semi-colon after the 1 because this is a vertical vector
    z2 = Theta2 * [1; output_layer1];
    output_layer2 = sigmoid(z2);

% Layer 3 process
% This layer is not a matrix multiplication, in other words we don't
% compute a linear approximation function here. What we do is to
% pick the maximum probability.

% If called with one input and two output arguments, `max' also
% returns the first index of the maximum value(s).
% p is a vertical vector where each i element is index to the max
% probability number in each row, this index is a number from 1 to 10
% and it is also the predicted category

% find the max of the vector, and assign the index of the max to p(i)
    [maxProb, p(i)] = max(output_layer2);

endfor
% =========================================================================


end
