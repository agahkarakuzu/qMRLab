function SimVaryPlot(SimVaryResults,Xaxis,Yaxis)

Xmin =  SimVaryResults.(Xaxis).x(1)  ;
Xmax =  SimVaryResults.(Xaxis).x(end);
Xmin = Xmin - (Xmax-Xmin)/50;
Xmax = Xmax + (Xmax-Xmin)/50;
X    =  SimVaryResults.(Xaxis).x;
Y    =  SimVaryResults.(Xaxis).(Yaxis).mean;
E    =  SimVaryResults.(Xaxis).(Yaxis).std;

cla;
hold on;
if (strcmp(Xaxis,Yaxis))
    plot([Xmin Xmax], [Xmin Xmax], 'k-');
else
    plot([Xmin Xmax],[SimVaryResults.(Xaxis).(Yaxis).GroundTruth SimVaryResults.(Xaxis).(Yaxis).GroundTruth], 'k-');
end
errorbar(X, Y, E, 'bo');

xlabel(sprintf('Input %s',  Xaxis), 'FontWeight', 'Bold');
ylabel(sprintf('Fitted %s', Yaxis), 'FontWeight', 'Bold');
xlim([Xmin Xmax]);
hold off;
grid('on');
