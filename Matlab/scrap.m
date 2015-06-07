%Just a scrap page for testing code

%createGif(phenoDataPath,'C:\Users\tstafford2\Desktop\tmp\oakville_timelapse.gif','oakville',sigfun);

rgbs = getImgs(phenoDataPath,'harvard',false);

gcc = zeros(1,length(rgbs)); datenms = zeros(1,length(rgbs)); doys = zeros(1,length(rgbs));
figure;
for i = 1:length(rgbs)
    %Read the image and calculate gcc. 
    rgb = imread(rgbs{i});
    rgbMask = maskSky(rgb,3);
    rgb = applyMask(rgb,rgbMask);
    imshow(rgb);
    gcc(i) = getGcc(rgb);
    [datenm,doy] = path2datenum(rgbs{i});
    datenms(i) = datenm;
    doys(i) = doy;
end

%% Read the climate data
fid = fopen('C:\Users\tstafford2\Desktop\tmp\harvard_climate.csv');
data = textscan(fid,'%s%f','Delimiter',',');
fclose(fid);

climDates = data{1};
temps = data{2};

climDoys = zeros(1,length(climDates));
for i = 1:length(climDates)
    cur = climDates{i};
    year = str2num(cur(1:4));
    month = str2num(cur(6:7));
    day = str2num(cur(9:10));
    t = datenum(year,month,day);
    climDoys(i) = datenum2fdoy(t);
end

%interp 
modTemps = interp1(climDoys,temps,doys,'nearest','extrap');

%try gridding the data...
[xq,yq] = meshgrid(1:365,-4:82);
vq = griddata(doys,modTemps,gcc,xq,yq);
figure; surf(xq,yq,vq);
