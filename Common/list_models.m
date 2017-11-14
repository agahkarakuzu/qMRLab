function [MethodList, pathmodels,ModelDir] = list_models
% list models
setenv('ISDISPLAY','0')
ModelDir = [fileparts(which('qMRLab.m')) filesep 'Models'];
[MethodList, pathmodels] = sct_tools_ls([ModelDir filesep '*.m'],0,0,2,1);
MethodList = MethodList(~strcmp(MethodList,'CustomExample'));