function [rgb,ir] = getImgs(dir,sitename,startDT,endDT,getIR)
    %Wrapper for the getsiteimglist function, because it is formatted
    %really oddly. This fetches rgb & ir images if desired. 
    
    if nargin < 2
      error('Not enough arguments specified');
    elseif nargin == 3
      startDT=datenum(1990,1,1);
      endDT=now;
      getIR = startDT;
    elseif nargin == 4
      getIR=false;
    end
        
    rgb = {}; ir = {};
    
    archive_dir = strcat(dir,'rgb/');
    rgb = getsiteimglist(archive_dir,sitename,startDT,endDT,false);
    
    if getIR
       archive_dir = strcat(dir,'ir/');
       ir = getsiteimglist(archive_dir,sitename,startDT,endDT,getIR);
    end
    
end