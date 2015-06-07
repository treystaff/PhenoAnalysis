%Matlab startup script.
% Do not modify this script without serious consideration. 
% Author: Trey Stafford
%% Add paths
addpath('O:\code\matlab\PhenoCam\');
addpath('O:\code\matlab\PhenoCam\phenocam_toolkit\');

%% Global variables
global phenoDataPath;
phenoDataPath = 'O:\PhenoCam\images\';

global sigfun
sigfun = @(F,x) F(1) + F(2)./ (1+exp(F(3) - F(4).*x));
