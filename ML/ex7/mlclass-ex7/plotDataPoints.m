function plotDataPoints(X, idx, K)
%PLOTDATAPOINTS plots data points in X, coloring them so that those with the same
%index assignments in idx have the same color
%   PLOTDATAPOINTS(X, idx, K) plots data points in X, coloring them so that those 
%   with the same index assignments in idx have the same color

% Create palette
palette = hsv(K + 1);
colors = palette(idx, :);

% Plot the data
% use idx directly. It will index into the default color map (64 colors)
% scatter(X(:,1), X(:,2), 15, colors);
scatter(X(:,1), X(:,2), 15, idx);

end
