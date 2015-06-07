function createGif(phenoDataPath,outpath,sitename,fun,varargin)
%Function for creating a .gif timelapse of PhenoCam GCC and NDVI over time. 

    %% Parse the inputs.
    p = inputParser;
    defaultStartDT = datenum(1990,1,1);
    defaultEndDT = now;
    defaultGetCir = true;
    defaultGetNDVI = true;
    defaultMask = [];
    
    %addRequired(p,'phenoDataPath');
    %addRequired(p,'outpath');
    %addRequired(p,'sitename');
    addOptional(p,'startDT',defaultStartDT);
    addOptional(p,'endDT',defaultEndDT);
    addOptional(p,'getCIR',defaultGetCir);
    addOptional(p,'getNDVI',defaultGetNDVI);
    addOptional(p,'mask',defaultMask);
    
    parse(p,varargin{:});
    %phenoDataPath = p.Results.phenoDataPath;
    %outpath = p.Results.outpath;
    startDT = p.Results.startDT;
    endDT = p.Results.endDT;
    %sitename = p.Results.sitename;
    getCIR = p.Results.getCIR;
    getNDVI = p.Results.getNDVI;
    mask = p.Results.mask;
    

    %% Function Logic

    %Get list of images.
    if getCIR || getNDVI %If CIR/NDVI is requested, get the IR images. 
        getIr = true;
    else
        getIr = false;
    end
    
    [rgbs,irs] = getImgs(phenoDataPath,sitename,startDT,endDT,getIr);
    if getNDVI
        ndvi = zeros(1,length(rgbs));
    end
    
    %Pre-Calculate desired metrics. 
    gcc = zeros(1,length(rgbs)); datenms = zeros(1,length(rgbs)); doys = zeros(1,length(rgbs));
    for i = 1:length(rgbs)
        %Read the image and calculate gcc. 
        rgb = imread(rgbs{i});
        rgbMask = maskSky(rgb,3);
        rgb = applyMask(rgb,rgbMask);
        gcc(i) = getGcc(rgb);
        if getNDVI
            %Read the IR image and calculate NDVI
            ir = imread(irs{i});
            ir = applyMask(ir,rgbMask);
            ndvi(i) = getNdvi(rgb,ir);
        end
        [datenm,doy] = path2datenum(rgbs{i});
        datenms(i) = datenm;
        doys(i) = doy;
    end
    
    [~, smonth] = month(datenms(1));
    [~, emonth] = month(datenms(end));
    
    params = fitSig(1:length(gcc),gcc,fun);

    %Check if doys(1) == min(doys). Multi-year not supported yet...lolol
    if doys(1) ~= min(doys)
        warning('MULTI-YEAR TIME SERIES. MAY NOT WORK PROPERLY W/OUT MODIFICATION');
    end
    
    %Now loop through all of the images again and construct the graphic.
    subRows = 1 + getCIR + getNDVI; %This defines the number of rows the plot will have.
    for i = 1:length(rgbs)
        subplots = []; %Track the subplots.
        %Create a reasonablly sized figure. 
        h = figure('position',[200,200,1000,700],'Visible','Off');   
        
        %Read the RGB image.
        rgb = imread(rgbs{i});
        rgb = applyMask(rgb,rgbMask);

        %Get the current date
        datenm = datenms(i);
        [~, m] = month(datenm);

        subplots = horzcat(subplots,subplot(subRows,2,1)); %RGB image will always take pos 1.
        imshow(rgb);
        axis image
        title(['RGB: ' m ' ' num2str(day(datenm))],'FontSize',11);

        %The color infrared image is optional. 
        if getCIR
            ir = imread(irs{i});
            ir = applyMask(ir,rgbMask);
            cir = getCir(rgb,ir);
           
            subplots = horzcat(subplots,subplot(subRows,2,3)); %This subplot is always in pos 3.
            imshow(cir);
            axis image
            title(['CIR: ' m ' ' num2str(day(datenm))],'FontSize',11);
        end

        if getNDVI
            ndviIm = getNdviIm(rgb,ir);
            ndviIm = applyMask(ndviIm,rgbMask);
            %The position of the NDVI image will either be pos 3 or pos 5
            if getCIR
                subplots = horzcat(subplots,subplot(subRows,2,5));
            else
                subplots = horzcat(subplots,subplot(subRows,2,3));
            end
            
            %Adjustments for good looks!
            imagesc(ndviIm); colorbar('westoutside');
            set(gca,'xtick',[]);set(gca,'ytick',[])
            set(gca,'xticklabel',[]);set(gca,'yticklabel',[])
            axis image
            pos = get(subplots(end),'position');
            %Need to offset this image to align w/ the others.
            pos(1) = pos(1) - 0.032; 
            set(gca,'position',pos);
            title(['NDVI: ' m ' ' num2str(day(datenm))],'FontSize',11);
        end
        
        linkaxes(subplots);

        %Finally, plot the graph of gcc/ndvi
        subplot(subRows,2,2:2:length(subplots)*2);   
        %plot(1:i,gcc(1:i),'b*');
        %
        plot(1:i,fun(params,1:i),'k-'); %at minimum, plot gcc & sigmoidal fit.
        hold on;
        if getNDVI
            [ax,~,~] = plotyy(1:i,gcc(1:i),1:i,ndvi(1:i),@(x,y)plot(x,y,'*','color',[0 0.5 0]),@(x,y)plot(x,y,'r*'));
            set(ax(1),'XLim',[0 length(rgbs)+1]);
            set(ax(2),'XLim',[0 length(rgbs)+1]);
            set(ax(1),'YLim',[min(gcc)-0.01 max(gcc)+0.01]);
            set(ax(1),'YTick',[min(gcc)-0.002:0.01:max(gcc)+0.002]);
            set(ax(2),'Ylim',[-1 1]);
            set(ax(2),'YTick',[-1:0.2:1]);
            ylabel(ax(1),'Green Chromatic Coordinate','FontSize',11);
            ylabel(ax(2),'NDVI','FontSize',11);            
            
            set(ax(1),'XTick',[0:10:length(rgbs)+1]);
            set(ax(2),'XTick',[0:10:length(rgbs)+1]);
            
            set(ax(1),'XTickLabel',[min(doys) - 1:10:max(doys) + 1]);
            set(ax(2),'XTickLabel',[min(doys) - 1:10:max(doys) + 1]);
            
            
            legend('Sigmoidal Fit','Image GCC','Mean NDVI','Location','northwest');
        else
            plot(1:i,gcc(1:i),'g*',1:i,fun(params,1:i),'k-');
            xlim([0 length(rgbs)+1]);
            set(gca,'YLim',[min(gcc)-0.002 max(gcc)+0.002]);
            set(gca,'XTickLabel',[min(doys) - 1:10:max(doys) + 1]);
            legend('Sigmoidal Fit','Image GCC','Location','northwest');
        end
   
        title([sitename ' ' smonth ' ' num2str(day(datenms(1)))...
            ' - ' emonth ' ' num2str(day(datenms(end)))],'FontSize',12);
        xlabel('DOY','FontSize',11);
        
        %Make the figure look nicer by removing unnecessary whitespace.
        tightfig(h);
        %Ensure that everthing has been drawn before saving the current
        % figure to .gif.
        drawnow;

        %Write the gif.
        frame = getframe(h);
        im = frame2im(frame);
        [a,map] = rgb2ind(im, 256);
        if i==1
            imwrite(a,map,outpath,'gif','LoopCount',Inf,'DelayTime',0.5);
        elseif i==length(rgbs)
            imwrite(a,map,outpath,'gif','WriteMode','append','DelayTime',5);
        else
            imwrite(a,map,outpath,'gif','WriteMode','append','DelayTime',0.5);
        end

        
        clf(h);
        close(h);
        
    end
end
