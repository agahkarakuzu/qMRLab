
classdef filter_map < AbstractModel & FilterClass
% filter_map:   Applies spatial filtering (2D or 3D)
%
% Assumptions:
%  
% Inputs:
%   Raw                Input data to be filtered
%   (Mask)             Binary mask to exclude voxels from smoothing
%
% Outputs:
%	Filtered           Filtered output map
%
% Protocol:
%	NONE
%
% Options: 
%   (inherited from FilterClass)
%   Smoothing Filter
%     Type                 Type of filter
%                              - gaussian
%                              - median
%     Dimension            In which dimensions to apply the filter
%                               -2D
%                               -3D
%     size(x,y,z)          Extent of filter in # of voxels
%                               For gaussian, it's FWHM
%
% Example of command line usage:
%
%   For more examples: <a href="matlab: qMRusage(filter_map);">qMRusage(filter_map)</a>
%
% Author: Ian Gagnon, 2017
%
% References:
%   Please cite the following if you use this module:
%     Cabana J-F, Gu Y, Boudreau M, Levesque IR, Atchia Y, Sled JG,
%     Narayanan S, Arnold DL, Pike GB, Cohen-Adad J, Duval T, Vuong M-T and
%     Stikov N. (2016), Quantitative magnetization transfer imaging made
%     easy with qMTLab: Software for data simulation, analysis, and
%     visualization. Concepts Magn. Reson.. doi: 10.1002/cmr.a.21357

    properties 
        MRIinputs = {'Raw','Mask'};
        xnames = {};
        voxelwise = 0; % 0, if the analysis is done matricially
        % 1, if the analysis is done voxel per voxel
        % Protocol
        Prot;
    end
    % Inherit these from public properties of FilterClass
    % Model options
    % buttons ={};
    % options = struct(); % structure filled by the buttons. Leave empty in the code
    
    methods
        % Constructor
        function obj = filter_map()
            obj.options = button2opts(obj.buttons);
        end
        
        function FitResult = fit(obj,data)
            % call the superclass (FilterClass) fit function
            data = data.Raw;
            FitResult.Filtered=struct2array(fit@FilterClass(obj,data,[obj.options.Smoothingfilter_sizex,obj.options.Smoothingfilter_sizey,obj.options.Smoothingfilter_sizez]));
        end
    
    end
    
end

