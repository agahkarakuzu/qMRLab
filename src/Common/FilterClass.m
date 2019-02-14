
classdef (Abstract) FilterClass
% FilterClass:  Methods for filtering data which can be inherited by other models
% Options:
%   Smoothing Filter
%     Type                 Type of filter
%                              - gaussian
%                              - median
%                              - spline
%                              - polynomial
%     Dimension            In which dimensions to apply the filter
%                               -2D
%                               -3D
%     size(x,y,z)          Extent of filter in # of voxels
%                               For gaussian, it's FWHM
%     order                Order of the polynomial fitting
    
    properties
        % Model options
        buttons ={'PANEL','Smoothing filter',6,...
            'Type',{'gaussian','median','spline','polynomial'},...
            'Dimension',{'3D','2D'},...
            'size x',3,...
            'size y',3,...
            'size z',3,...
            'order',12};
        options = struct(); % structure filled by the buttons. Leave empty in the code
    end
    
    methods
        % Constructor
        function obj = FilterClass()
        end
        function obj = UpdateFields(obj)
          
            % Disable/enable some options --> Add ### to the button
            % Name you want to disable
            disablelist = {'size x','size y','size z','order'};
            switch  obj.options.Smoothingfilter_Dimension
                case {'2D'}
                    disable = [false false true true]; 
                    obj.options.Smoothingfilter_sizez=0;
                otherwise
                   disable = [false false false true]; 
            end
            % for spline, only 1 value for the amount of smoothness and 3D
            if strcmp(obj.options.Smoothingfilter_Type,{'spline'})
                disable = [false true true true]; 
            end
            % for polynomial, now polynomial fitting works for both 2D and
            % 3D cases
            if strcmp(obj.options.Smoothingfilter_Type,{'polynomial'})
                disable = [true true true false];
%                 obj.options.Smoothingfilter_Dimension={'2D'};
            end
            
            for ll = 1:length(disablelist)
                indtodisable = find(strcmp(obj.buttons,disablelist{ll}) | strcmp(obj.buttons,['##' disablelist{ll}]));
                if disable(ll)
                    obj.buttons{indtodisable} = ['##' disablelist{ll}];
                else
                    obj.buttons{indtodisable} = [disablelist{ll}];
                end
            end
        end
        
        function FitResult = fit(obj,data,size)
            switch obj.options.Smoothingfilter_Type
                case {'gaussian'}
                    FitResult.Filtered=obj.gaussFilt(data,size); %smoothed
                case {'median'}
                    FitResult.Filtered=obj.medianFilt(data,size); %smoothed
                case {'spline'}
                    FitResult.Filtered=obj.splineFilt(data,size); %smoothed
                case {'polynomial'}
                    FitResult.Filtered=obj.polyFilt(data,obj.options.Smoothingfilter_order); %smoothed
            end
        end
        % Gaussian filter
        function filtered = gaussFilt(obj,data,fwhm)
            % Apply a Gaussian filter (2D or 3D)
            % fwhm is a 2 or 3-element vector of positive numbers
            sigmaPixels = fwhm2sigma(fwhm); %Full width half max of desired gaussian kernel (in #voxels) converted to sigma of Gaussian
            if(sigmaPixels(3)==0 || strcmp(obj.options.Smoothingfilter_Dimension,'{2D}')) %for the 2D case
                filtered = imgaussfilt(data,sigmaPixels(1:2));
            else
                filtered = imgaussfilt3(data,sigmaPixels);
            end
        end
        
        %Median filter
        function filtered =medianFilt(obj,data,s)
            % Apply a median filter (2D or 3D)
            % s is a 3-element vector of positive numbers (voxels)
            if(s(3)==0 || strcmp(obj.options.Smoothingfilter_Dimension,'{2D}')) %for the 2D case, if the volume is 3D, have to do each slice separately
                if(ndims(data)==2)
                    filtered = medfilt2(data,s(1:2));
                else
                    filtered=zeros(size(data));
                    for i=1:size(data,3)
                        filtered(:,:,i)=medfilt2(data(:,:,i),s(1:2));
                    end
                end
            else
                filtered = medfilt3(data,s);
            end
        end
        
        %Spline filter
        function filtered =splineFilt(obj,data,S)
            % Apply a spline filter (2D or 3D)
            s=S(1); %just 1 values for the smoothness
            if(strcmp(obj.options.Smoothingfilter_Dimension,'{2D}')) %if want 2D smoothing
                if(ndims(data)==2) %if a 2D volume
                    filtered = smoothn(data,s);
                else %if a 3D volume, do each slice separately
                    filtered=zeros(size(data));
                    for i=1:size(data,3)
                        filtered(:,:,i)=smoothn(data(:,:,i),s);
                    end
                end
            else
                filtered = smoothn(data,s);
            end
                
            %filtered = smoothn(data,'robust');            
        end
        
        %Polynomial filter
        function filtered=polyFilt(obj,data,order)
            % Apply a polynomial fit of the specified order (in 2D)
            if(ndims(data)==2) %if a 2D volume
                filtered = poly_fit(data,order);
            % if a 3D volume, use 2D or 3D fit according to the selection of dimension:
            % 1. Perform each slice separately in 2D poly fit; OR
            % 2. Perform 3D poly fit
            else
                filtered=zeros(size(data));
                if strcmp(obj.options.Smoothingfilter_Dimension,'{2D}')
                    for i = 1:size(data,3)
                        filtered(:,:,i) = poly_fit(data(:,:,i),order);
                    end
                else
                    filtered = polyfit_3D(data(:,:,i),order);
                end
            end
        end
        
    end
    
    
    
end

