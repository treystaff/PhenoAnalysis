%Just a script for testing difference between mask & full image.
% This is a proof of concept and should be extensiviely reviewed/revised if
% used for anything serious. 

%% USER INPUT
sitename = 'harvard';
year = 2014;
decimate = 1;

%% AUTOMATED
mask = imread(strcat(phenoDataPath,sitename,'/mask.tif'));
%For some reason, the phenocam site reverses mask conventions, fix: 
mask = logical(~mask);

%Get images list:
imgs = getsiteimglist(phenoDataPath,'rgb/',sitename);

vari = []; gcc = [];
mVari = []; mGcc = [];
mMGcc = []; %Mean Masked GCC
for i = 1:decimate:length(imgs)
    %Read the current image.
    img = imread(imgs{i});
    
    %Extract individual rgb channels. 
    red = double(img(:,:,1));
    green = double(img(:,:,2));
    blue = double(img(:,:,3));
    
    %Calculate based on sum of values instead of mean or something else for
    %now
    %get vari & gcc w/out mask 
    vari = horzcat(vari, (sum(green) - sum(red)) / (sum(green) + sum(red) + sum(blue))); %vari
    gcc = horzcat(gcc, sum(green) / (sum(green) + sum(red) + sum(blue))); %gcc
    
    %get vari & gcc w/ mask
    green = green(mask);
    red = red(mask);
    blue = blue(mask);
    mVari = horzcat(mVari, (sum(green) - sum(red)) / (sum(green) + sum(red) + sum(blue))); %vari
    mGcc = horzcat(mGcc, sum(green) / (sum(green) + sum(red) + sum(blue))); %gcc
    
    %Get the mean masked GCC
    mMGcc = horzcat(mMGcc, mean(green) / (mean(green) + mean(red) + mean(blue))); %gcc
    
end

%For now, just want to see the trend, nothing fancy. 
x = 1:length(imgs);
figure; plot(x,vari,'g-');hold on; plot(x,mVari,'r-');title('vari vs mVari');legend('vari','mVari');
figure; plot(x,gcc,'g-');hold on; plot(x,mGcc,'r-');title('gcc vs mGcc');legend('gcc','mGcc');
figure; plot(x,mGcc,'g-');hold on; plot(x,mMGcc,'r-');title('mGcc vs mMGcc');legend('mGcc','mMGcc');