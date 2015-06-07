function maskImg = applyMask(img,mask)
%Applys a mask to the given image

    [~,~,nd] = size(img);
    if nd == 3
        red = img(:,:,1);
        green = img(:,:,2);
        blue = img(:,:,3);

        red(~mask) = NaN;
        green(~mask) = NaN;
        blue(~mask) = NaN;

        maskImg = img;
        maskImg(:,:,1) = red;
        maskImg(:,:,2) = green;
        maskImg(:,:,3) = blue;
    elseif nd == 1
        maskImg = img;
        maskImg(~mask) = NaN;
    else
        error('Number of image channels must be 1 or 3');
    end
end
