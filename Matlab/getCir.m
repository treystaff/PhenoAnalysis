function cir = getCir(rgb,ir)
    % cir = getCir(rgb,ir)
    % 
    % Returns a nice color infrared image useful for visualiziation.
    % cir = Color InfraRed. Image with IR,Red, and Green channels. 
    %
    % Input: 
    %   rgb: A PhenoCam rgb image.
    %   ir: A PhenoCam IR image. 
    %
    % Output:
    %   cir: A Color infrared image.   
    % 
    % Notes: Pretty images!
    % See also: getNdvi.m
    
    %Extract the red and green channels from the rgb image
    red = rgb(:,:,1);
    green = rgb(:,:,2);
    
    %Extract one of the bands from the IR image. 
    nir = ir(:,:,1);
    
    %Create the CIR image. 
    cir = rgb;
    cir(:,:,1) = nir;
    cir(:,:,2) = red;
    cir(:,:,3) = green;
    
end