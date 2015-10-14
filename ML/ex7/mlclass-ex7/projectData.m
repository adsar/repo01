function Z = projectData(X, U, K)
%PROJECTDATA Computes the reduced data representation when projecting only 
%on to the top k eigenvectors
%   Z = projectData(X, U, K) computes the projection of 
%   the normalized inputs X into the reduced dimensional space spanned by
%   the first K columns of U. It returns the projected examples in Z.
%

% You need to return the following variables correctly.
Z = zeros(size(X, 1), K);

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the projection of the data using only the top K 
%               eigenvectors in U (first K columns). 
%               For the i-th example X(i,:), the projection on to the k-th 
%               eigenvector is given as follows:
%                    x = X(i, :)';
% the row vector x above is transposed just for convention,
% so that it becomes a vertical vector, by convention all vectors are vertical
%                    projection_k = x' * U(:, k);
% note that this formula uses x', which means that we transpose it back so
% it is a row vector, and in that way t can be multiplied by the
% column U(:, k)
%

Z = X * U(:, 1:K);


% =============================================================

end
