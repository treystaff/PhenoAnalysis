function [dnum, doy] = path2datenum(path,ir)
    % [dnum, doy] = path2datenum(path,ir)
    % 
    % Returns the datenum and doy of the image for the given filepath. 
    %
    % Input: 
    %   path: PhenoCam image filepath. 
    %   ir: boolean flag for IR images (optional). 
    %
    % Output:
    %   params: vector of parameter values.
    % 
    % See also: fn2datenum, datenum2fdoy, datevec

    %Parse the filename and sitename from the filepath because its annoying
    %to type the sitename everytime. 
     [~,name,ext] = fileparts(path);
    if nargin < 2 || ~ir
        regex = '_[0-9]{4}_';
        ir = false;
    else
        regex = '_IR_[0-9]{4}_';
        ir = true;
    end
   
    sitename = name(1:regexp(name,regex) - 1);
    
    dnum = fn2datenum(sitename,[name ext],ir);
    doy = datenum2fdoy(dnum);     
end