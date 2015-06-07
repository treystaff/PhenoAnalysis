function midpoint = getVertMidpt(x,y)
    % midpoint = getVertMidpt(x,y)
    % 
    % Returns the midpoint of the sigmoidal function's vertical spring
    % rise. 
    %
    % Input: 
    %   x: Vector, independent variable (can just be 1:length(images)
    %   y: Vector of values for the dependent variable (gcc)
    %
    % Output:
    %   midpoint: the x location of the midpoint of the sig's vertical. 
    % 
    % Notes: This was created after fitSig. Maybe just combine them, not
    % sure if it is necessary to have two functions for this?
    % See also: fitSig.m
    
    params = fitSig(x,y);
    midpoint = params(3)/params(4);
    
end