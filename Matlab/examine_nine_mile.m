%Script to look at the ninemile prairie. Just a test script.

%Get the images
[rgbs,irs] = getImgs(phenoDataPath,'ninemileprairie',true);

gcc = []; ndvi = [];
x = 106:126;
for i = 1:length(rgbs)
    rgb = imread(rgbs{i});
    ir = imread(irs{i});
    gcc = horzcat(gcc,getGcc(rgb));
end
% ts = timeseries(gcc,x);
% ts.Name = 'Green Chromatic Coordinate';
% ts.TimeInfo.Units = 'days';
% ts.TimeInfo.StartDate = '04/16/2015';
% ts.TimeInfo.Format = 'mmm dd, yy';
% ts.Time = ts.Time - ts.Time(1);
% 
% figure;plot(ts,'b*');legend('GCC'); ylabel('GCC'); xlabel('Date');
% title('Nine Mile Green Chromatic Coordinate: 4/16 - 5/6');
