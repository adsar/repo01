function [bestEpsilon bestF1] = selectThreshold(yval, pval)
%SELECTTHRESHOLD Find the best threshold (epsilon) to use for selecting
%outliers
%   [bestEpsilon bestF1] = SELECTTHRESHOLD(yval, pval) finds the best
%   threshold to use for selecting outliers based on the results from a
%   validation set (pval) and the ground truth (yval).
%

bestEpsilon = 0;
bestF1 = 0;
F1 = 0;

stepsize = (max(pval) - min(pval)) / 1000;
for epsilon = min(pval):stepsize:max(pval)
    
    % ====================== YOUR CODE HERE ======================
    % Instructions: Compute the F1 score of choosing epsilon as the
    %               threshold and place the value in F1. The code at the
    %               end of the loop will compare the F1 score for this
    %               choice of epsilon and set it to be the best epsilon if
    %               it is better than the current choice of epsilon.
    %               
    % Note: You can use predictions = (pval < epsilon) to get a binary vector
    %       of 0's and 1's of the outlier predictions


% pval and yval a vectors of probabilities;
% pval is the probablity density computed by gaussian model for each validation example,
%      pval(i) must be interpreted as the probablity that X(i,:) is a normal example.

% yval is a boolean value (0 or 1), is the label of each training example (aka "ground truth")
% Above I took the liberty of calling it a probablity, in the sense that booleans
% can be seen as a special case of probabily distribution.
%      yval(i) can be interpreted as the probablity that X(i,:) is a normal example.

% I use Octave less-than test between a vector and a single number to obtain a boolean vector
% of all the cases when teh probability of normal case is less than epsilon
prediction = (pval < epsilon);


% I use Octave's equality test between a vector and a single number to count cases:

% true positives
tp = sum((prediction == 1) & (yval == 1));

% false positive
fp = sum((prediction == 1) & (yval == 0));

% false negatives
fn = sum((prediction == 0) & (yval == 1));

% precission (credibility of the system when it gives a positive, how many diagnosed possitives are real)
prec = tp / (tp + fp);

% recall (detection power of the system, how many real possitives it didn't miss)
rec = tp / (tp + fn);

% F1 score
F1 = 2 * prec * rec / (prec + rec);

    % =============================================================

    if F1 > bestF1
       bestF1 = F1;
       bestEpsilon = epsilon;
    end
end

end
