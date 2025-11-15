function rgb = ind2rgb8(ind, cmap)
% IND2RGB8 Convert indexed image to RGB image (uint8)
%
% RGB = IND2RGB8(IND, CMAP) converts the indexed image IND with colormap
% CMAP to an RGB image. This is a pure MATLAB implementation that does
% not require the Mapping Toolbox or compiled MEX files.
%
% This function is compatible with MATLAB R2019b and newer versions.
%
% Inputs:
%   IND  - Indexed image (2D array) with integer indices
%   CMAP - Colormap (Nx3 array) with RGB values in range [0, 1]
%
% Output:
%   RGB  - RGB image (HxWx3 uint8 array)
%
% Note: This is a fallback implementation for use when MEX files are
%       not available or when the Mapping Toolbox is not installed.

% Input validation
if nargin < 2
    error('ind2rgb8:wrongNumInputs', 'Two input arguments required.');
end

if ~isnumeric(ind) || ndims(ind) > 2
    error('ind2rgb8:invalidInput', 'IND must be a 2D numeric array.');
end

if ~isnumeric(cmap) || size(cmap, 2) ~= 3
    error('ind2rgb8:invalidMap', 'CMAP must be an Nx3 numeric array.');
end

% Get image dimensions
[height, width] = size(ind);

% Ensure colormap values are in [0, 1] range
if max(cmap(:)) > 1 || min(cmap(:)) < 0
    warning('ind2rgb8:colormapRange', 'Colormap values should be in [0, 1] range. Clipping values.');
    cmap = max(0, min(1, cmap));
end

% Clamp indices to valid colormap range [1, size(cmap,1)]
ind = double(ind);
ind = max(1, min(size(cmap, 1), ind));

% Round indices to integers
ind = round(ind);

% Initialize RGB output
rgb = zeros(height, width, 3, 'uint8');

% Map indexed values to RGB using the colormap
% This is equivalent to ind2rgb but optimized for uint8 output
for k = 1:3
    % Create a temporary array for this color channel
    temp = cmap(ind, k);
    % Scale from [0,1] to [0,255] and convert to uint8
    rgb(:, :, k) = uint8(temp * 255);
end

end
