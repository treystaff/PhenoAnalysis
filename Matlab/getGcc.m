function gcc = getGcc(img)
    % gcc = getGcc(img)
    % 
    % Returns the green chromatic coordinate from an image with rgb bands.
    % GCC = GREEN / (RED + GREEN + BLUE)
    %
    % Input: 
    %   img: an image read into matlab w/ imread(). Should be an n*m*3
    %   matrix. 
    %
    % Output:
    %   gcc: the calculated gcc for the entire image. 
    % 
    % Notes: I think some use mean instead of sum, but this may give
    % appximately the same results? Look into/change if necessary. 
    % See also: getNdvi.m

    %Extract individual rgb channels. 
    red = nansum(double(img(:,:,1)));
    green = nansum(double(img(:,:,2)));
    blue = nansum(double(img(:,:,3)));
    
    %Calculate based on sum of values instead of mean or something else for
    %now
    gcc = green / (red + green + blue);
    
end