function params = fitSig(x,y,sigfun)
    % params = fitSig(x,y)
    % 
    % Returns a vector of estimated parameter values for the sigmoidal 
    %   function used in Richardson 07.
    %
    % Input: 
    %   x: Vector, independent variable (can just be 1:length(images)
    %   y: Vector of values for the dependent variable (gcc)
    %
    % Output:
    %   params: vector of parameter values.
    % 
    % Notes: This works best for modeling greenup in the spring. Probably
    % want to truncate the end of the dataset to remove the Fall. Choosing
    % where to perform the truncation may be tricky...
    % See also: getVertMidpt.m

    %Define the function (Richardson 07)
    sigfun = @(F,x) F(1) + F(2)./ (1+exp(F(3) - F(4).*x));
    fitted = nlinfit(x,y,sigfun,[1 1 1 1]); %Use a base vector of 1's to start w/...
    
    %Plot the result
    %figure; plot(x,y,'*',x,sigfun(fitted,x),'g'),legend('data','fit');
    
    %Return results
    params = fitted;
end