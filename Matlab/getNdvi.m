function ndvi = getNdvi(rgb,ir)
    % ndvi = getNdvi(rgb,ir)
    % 
    % Returns the camera's NDVI value for the image.
    % NDVI = (NIR - RED) / (NIR + RED)
    %
    % Input: 
    %   rgb: A PhenoCam rgb image.
    %   ir: A PhenoCam IR image. 
    %
    % Output:
    %   ndvi: camera calculated NDVI.  
    % 
    % Notes: This isn't exactly NDVI as it is calculated by other sensors.
    % The IR image is really some mixture of IR + RGB. Gives nice looking
    % result and may nevertheless be helpful, however. More info/testing
    % necessary.
    % See also: getNdvi.m
    
    %Extract the red channel from the rgb image
    red = nanmean(double(rgb(:,:,1)));
    
    %Extract one of the bands from the IR image. 
    nir = nanmean(double(ir(:,:,1)));
    
    %Calculate camera NDVI
    ndvi = (nir-red) / (nir+red);
end