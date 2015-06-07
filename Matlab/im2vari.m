function variImg = im2vari(img)
%Creates a VARI index image. 

    [nr,nc,nd] = size(img);
    if nd ~= 3
        error('Passed image/matrix must have 3 channels (red, green, blue)');
    end
    
    red = double(img(:,:,1));
    green = double(img(:,:,2));
    blue = double(img(:,:,3));
    
    variImg = (green - red) ./ (green + red + blue);    
end
