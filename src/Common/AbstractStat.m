classdef (Abstract) AbstractStat
    
    
    % AbstractModel:  Properties/Methods shared between all models.
    %
    %   *Methods*
    %   save: save model object properties to a file as an struct.
    %   load: load model properties from a struct-file into the object.
    %
    
    properties
        
        Map
        MapNames
        NumMaps
        
        StatMask
        StatLabels
        StatMaskFolder
        
        UsrLabels
        StatID
        
        FitMask
        
        ProbMask
        ProbMaskFolder 
        
        ModelName
        ModelVersion
        StatVersion
        
    end
    
    properties (Hidden=true)
        
        FitMaskName
        
    end
    
    methods
        
        function obj = AbstractStat()
            obj.StatVersion = qMRLabVer();
        end
        
        
        function obj = getStatMask(obj,input)
            % A stat mask can be a labeled mask or a binary mask.
            
            if ~isempty(inputname(1)) && exist(inputname(1),'var') ==1 % Var from workspace
                
                obj.StatMask = evalin('base',inputname(1));
                [obj.StatMask,obj.StatLabels] = AbstractStat.maskAssignByType(obj.StatMask);
                
            elseif exist(input,'file') == 2 % File
                
                obj.StatMask = AbstractStat.loadFile(input);
                [obj.StatMask,obj.StatLabels] = AbstractStat.maskAssignByType(msk);
                
            elseif exist(input,'file') == 7 % Folder
                
                % This folder should contain unified format.
                % If len>2 all inputs should be binary.
                
                obj.StatMaskFolder = input;
                [obj.StatMask, obj.StatLabels] = AbstractStat.getFileContent(input);
                
            else
                
                error('Provided input is NOT i) a variable in workspace, ii) a file or iii) a folder.');
                
            end
            
            
            
        end
        
        
        function obj = getProbmask(obj,input)
            
            if ~isempty(inputname(1)) && exist(inputname(1),'var') ==1 % Var from workspace
                
                obj.ProbMask = evalin('base',inputname(1));
                
            elseif exist(input,'file') == 2 % File
                
                obj.ProbMask = AbstractStat.loadFile(input);
                
            elseif exist(input,'file') == 7 % Folder
                                
                obj.ProbMaskFolder = input;
                [obj.ProbMask, ~] = AbstractStat.getFileContent(input);
                
            else
                
                error('Provided input is NOT i) a variable in workspace, ii) a file or iii) a folder.');
                
            end
            
            
        end
        
        
        function obj = loadByFitResults(obj,filename,varargin)
            
            results = load(filename);
            fnames = fieldnames(results);
            
            if ~all(ismember({'Model','Version'},fnames))
                
                error('The file is not associated with a qMRLab output.');
                
            end
            
            obj.ModelName = results.Model.ModelName;
            obj.ModelVersion = results.Version;
            
            if ismember({'Files'},fieldnames(results)) && ismember('Mask',fieldnames(results.Files));
                
                obj.FitMaskName = results.Files.Mask;
                
            end
            
            % You loaded mask, you should also load maps. 
            
            if nargin==2 % load all maps 
                
               
               
               idx = ismember(results.Model.xnames,fnames);
               obj.MapNames = results.Model.xnames(idx);
               tmp = results.(results.Model.xnames{1});
                            
               [mapin, dim] = AbstractStat.getEmptyVolume(size(tmp),length(obj.MapNames));
               
               if dim == 2
               for ii=1:length(obj.MapNames)
                   
                  mapin(:,:,ii) = results.(obj.MapNames{ii});
                   
               end
               
               elseif dim ==3
                   
                for ii=1:length(obj.MapNames)
                   
                  mapin(:,:,:,ii) = results.(obj.MapNames{ii});
                   
               end    
                   
               end
               
               obj.Map = mapin;
               
            elseif nargin>2 % load selected maps 
                
                tmp = results.(results.Model.varargin{1});
                obj.MapNames = varargin;
                
               [mapin, dim] = AbstractStat.getEmptyVolume(size(tmp),length(obj.MapNames));
               
               if dim == 2
               for ii=1:length(obj.MapNames)
                   
                  mapin(:,:,ii) = results.(obj.MapNames{ii});
                   
               end
               
               elseif dim ==3
                   
                for ii=1:length(obj.MapNames)
                   
                  mapin(:,:,:,ii) = results.(obj.MapNames{ii});
                   
               end    
                   
               end
               
            end
                
            obj.Map = mapin; 
            obj.NumMaps = length(obj.MapNames);
            
            
        end
        
        
        function obj = getFitMask(obj)
            
            if isempty(obj.FitMaskName)
                
                error('FitResults is not loaded into statistics object yet, OR Mask is not present in the loaded FitResults.')
                
            end
            
            try
                
                % FitMask is always logical assumption here 
                % Change if one day someone is fitting with labeled masks. 
                
                obj.FitMask = logical(AbstractStat.loadFile(obj.FitMaskName));
                                
            catch
                
                error('The Mask file cannot be located on your computer.');
                
            end
                        
            
        end
        
        
        
        
        
    end
    
    
    
    
    methods (Static, Hidden=true)
        
        
        
        function fType = getInpFormat(fileName)
            
            loc = max(strfind(fileName, '.'));
            
            frm = fileName(loc+1:end);
            
            if strcmp(frm,'gz') || strcmp(frm,'nii')
                
                fType = 'nifti';
                
            elseif strcmp(frm,'mat')
                
                fType = 'matlab';
                
            end
            
        end
        
        
        
        function [out,labels] = maskAssignByType(mask)
            
            
            members = unique(mask(:));
            
            if length(members) > 2 % labeledmask
                
                members(members==0) = []; % Remove 0 from the list
                labels = num2cell(sort(members));
                out = mask; 
                
            elseif length(members) == 2
                
                out = logical(mask);
                labels = [];
            
            end
            
            
            
        end
        
        
        
        
        
        function output = loadFile(input)
            
            
            
            switch AbstractStat.getInpFormat(input)
                
                
                case 'nifti'
                    
                    try
                        
                        output = load_nii_data(input);
                        
                    catch
                        
                        output = load_nii(input);
                        
                        output = output.img;
                        
                    end
                    
                case 'matlab'
                    
                    im = load(input);
                    output = im.(cell2mat(fieldnames(im)));
                    
            end
            
            
            
            
        end
        
        function [out, label] = getFileContent(path)
           
        matList  = dir(fullfile(path,'*.mat'));
        niiList1 = dir(fullfile(path,'*.nii.gz'));
        niiList2 = dir(fullfile(path,'*.nii'));
        
        if isempty(niiList1) && isempty(niiList2) && isempty(matList)
        
            error('Directory does not contain any files with recognized formats (.mat, .nii.gz, .nii).');
        
        elseif (~isempty(niiList1) || ~isempty(niiList2)) && (isempty(matList)) % Nifti masks
                    
            if ~isempty(niiList1) && ~isempty(niiList2)
                
                readList = {niiList1.name niiList1.name};
                [out, label] = AbstractStat.readUniFormat(readList);
                
            elseif ~isempty(niiList1)
               
                readList = {niiList1.name};
                [out, label] = AbstractStat.readUniFormat(readList);
                
            elseif ~isempty(niiList2)
                
                readList = {niiList2.name};
                [out, label] = AbstractStat.readUniFormat(readList);
                
            else
                
                
                
            end
            
        elseif (isempty(niiList1) && isempty(niiList2)) && (~isempty(matList)) % mat masks   
           
            readList = {matList.name};
            [out, label] = AbstractStat.readUniFormat(readList);
            
        else
            
            error('Mask folder contents shoud share the same format.');
            
        end    
        
        
            
        end
        
        
        function [out, label] = readUniFormat(readlist)
           
            
            if length(readlist) == 1 
                
                out = AbstractStat.loadFile(readlist{1});
                [out,label] = AbstractStat.maskAssignByType(out);
                
                if isempty(label)
                    label = AbstractStat.strapFileName(readlist{1});
                end
            
            else
                
            tmp = AbstractStat.loadFile(readlist{1});
            sz = size(tmp); 
            label = cell(length(readlist),1);
            
            if length(sz)>2
                
                 out   = zeros(sz(1),sz(2),sz(3));              
                 
                                
            elseif length(sz) == 2
              
                 out = zeros(sz(1),sz(2));
                
            end
            
           
            for ii=1:length(readlist)
                 
                 curMask = AbstractStat.loadFile(readlist{ii});
                 out(curMask==1) = ii;
                 label{ii} = AbstractStat.strapFileName(readlist{ii});
                 
             end
            
           
            end
            
        end
        
        
        function  out = strapFileName(in)
                         
             locpt = strfind(in, '.');
             out = in(1:(locpt-1));
             
            
        end
        
        function [vol, dim] = getEmptyVolume(sz,len)
            
            ln = length(sz);
            
            if ln == 2
                
                vol = zeros(sz(1),sz(2),len);
                dim  = 2;
                
            elseif ln>2 
               
                vol = zeros(sz(1),sz(2),sz(3),len);
                dim = 3;
            end
            
            
        end
        
    end
    
    
    
    
    
    
    
    
end