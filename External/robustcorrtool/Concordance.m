function [rC,biasFactorC,hboot,CIC,hout] = Concordance(X,Y,XLabel,YLabel,fig_flag,alpha_level)

  svds = struct();

  nboot = 1000;

  if size(X,1) == 1 && size(X,2) > 1; X = X'; end
  if size(Y,1) == 1 && size(Y,2) > 1; Y = Y'; end

      if size(X,2) == 1 && size(Y,2) > 1
        X = repmat(X,1,size(Y,2));
      elseif size(Y,2) == 1 && size(X,2) > 1
        Y = repmat(Y,1,size(X,2));
      end

      if sum(size(X)~=size(Y)) ~= 0
        error('X and Y must have the same size')
      end

      %% parameters
      if nargin < 2
        error('two inputs requested');
      elseif nargin == 2
        % #qmrstat
        alpha_level = 5/100;
      elseif nargin == 5
        % #qmrstat
        alpha_level = 5/100;
      end

      Z = [X,Y];
      [n ~] = size(Z);

      S = cov(Z,1);
      ybar = mean(Z);
      shiftC = (ybar(1)-ybar(2))/(sqrt(sqrt(S(1,1))*sqrt(S(2,2))));
      scaleC = sqrt(S(1,1))/sqrt(S(2,2));
      biasFactorC = ((scaleC+1/scaleC+shiftC^2)/(2))^-1;

      Var1 = S(1,1); Var2 = S(2,2); S = S(1,2);
      rC = (2.*S) ./ ( Var1 +Var2 + (ybar(1)-ybar(2))^2);

      if nargout > 1

        go = 1;

        while go == 1

          table = randi(n,n,nboot);

          rCB = zeros(1,nboot);
          for b=1:nboot
            S = cov(Z(table(:,b),:),1); Var1 = S(1,1); Var2 = S(2,2); S = S(1,2);
            rCB(b) = (2.*S) ./ ( Var1 +Var2 + (mean(Z(table(:,b),1))-mean(Z(table(:,b),2)))^2);
          end
          rCB = sort(rCB);
          adj_nboot = nboot - sum(isnan(rCB));
          low = round((alpha_level*adj_nboot)/2); % lower bound
          high = adj_nboot - low; % upper bound
          rCB(isnan(rCB)) = [];
          CIC = [rCB(low) rCB(high)];
          if  rC>CIC(1) && rC<CIC(2)
            go = 0;
          end
        end
      end

      if fig_flag ~= 0

        if nargout == 5
          hout = figure('Name','Concordance correlation');
          set(gcf,'Color','w');
          set(hout,'Visible','off');

        else % When hout is not a nargout

          figure('Name','Concordance correlation');
          set(gcf,'Color','w');

        end

        if moxunit_util_platform_is_octave
        scatter(X,Y,10,'filled');
        else
        scatter(X,Y,100,'filled');
        end

        grid on; hold on;
        xlabel(XLabel,'FontSize',14); ylabel(YLabel,'FontSize',14);
        title(['Concordance corr =' num2str(rC) ' Bias factor: ' num2str(biasFactorC)],'FontSize',16);

        v = axis;
        intsect = range_intersection([v(1) v(2)],[v(3) v(4)]);

        if min(CIC)<0 && max(CIC)>0
            hboot = 0;
        else
            hboot = 1;
        end

        if ~isempty(intsect)

            identity = intsect(1):intsect(2);
            plot([identity(1),identity(end)],[identity(1),identity(end)],'k--','LineWidth',3);

            if moxunit_util_platform_is_octave

              [x_bfl,y_bfl] = lsline_octave(X,Y,gca(),'r',2);
              svds.Required.shiftedLine = [x_bfl,y_bfl];

            else

              h=lsline; set(h,'Color','r','LineWidth',2);

              svds.Required.shiftedLine = [get(h,'XData'),get(h,'YData')];
            end

            svds.Required.identityLine = [identity(1),identity(end),identity(1),identity(end)];

        else

           disp(['Concordance and identity lines cannot be drawn: ' cell2mat(XLabel) ' vs ' cell2mat(YLabel)]);
           svds.Required.identityLine = [];
           svds.Required.shiftedLine  = [];

        end




      end

      assignin('caller','svds',svds);
end
