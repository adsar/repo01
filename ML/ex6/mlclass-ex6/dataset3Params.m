function [C, sigma] = dataset3Params(X, y, Xval, yval)
%EX6PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = EX6PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
C = 1.0;
sigma = 1.0;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%
tolerance = 1e-3;
max_iterations = 20;
min_C = 0.0;
min_sigma = 0.0;
min_prediction_error = 1000000;
steps = [0.01 0.03 0.1 0.3 1 3 10 30];
fprintf(['dataset3Params: size(steps,2) = %f.\n'], size(steps,2));
for i = 1 : size(steps,2)
    for j = 1 : size(steps,2)
        Ci = C * steps(i);
        sigmaj = sigma * steps(j);
        % x1 and x2 are placeholders for the function arguments. You don't have to calculate them.
        % @(x1, x2) gaussianKernel(x1, x2, sigma) is  just a trick - it is a definition of an anonymous function which takes 2 parameters (x1 and x2) and passes them to gaussianKernel().
        model = svmTrain(X, y, Ci, @(x1, x2) gaussianKernel(x1, x2, sigmaj),
                         tolerance, max_iterations);
        predictions = svmPredict(model, Xval);
        prediction_error = mean(double(predictions ~= yval));
        fprintf(['dataset3Params: C = %f, sigma = %f, prediction error on validation set = %f.\n'], Ci, sigmaj, prediction_error);
        if (min_prediction_error > prediction_error)
            min_prediction_error = prediction_error;
            min_C = Ci;
            min_sigma = sigmaj;
        endif
    endfor
endfor
fprintf(['dataset3Params: OPTIMAL: C = %f, sigma = %f, prediction error on validation set = %f.\n'], min_C, min_sigma, min_prediction_error);

C = min_C;
sigma = min_sigma;

% =========================================================================

end
