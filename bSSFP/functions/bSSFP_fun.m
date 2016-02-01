function My = bSSFP_fun( x, xdata, FitOpt )
% bSSFP_fun Analytical bSSFP solution for pre determined W. 
% Used for fitting data points with fixed W because calculation of W takes time
% x = [F,kr,R1f,R1r,T2f,M0f]
% xdata = [alpha, Trf, TR, W]

% Reference: M. Gloor, K. Scheffler, and O. Bieri. "Quantitative
% Magnetization Transfer Imaging Using Balanced SSFP", Magnetic Resonance
% in Medicine 60:691–700 (2008)

alpha = xdata(:,1)*pi/180;
Trf   = xdata(:,2);
TR    = xdata(:,3);
W     = xdata(:,4);

F   = x(1);
kr  = x(2);
R1f = x(3);
R1r = x(4);
T2f = x(5);
M0f = x(6);
kf  = kr .* F;
R2f = 1 ./ T2f;

if ( FitOpt.R1reqR1f )
     R1r = x(3);
end

if (isfield(FitOpt,'R1') && ~isempty(FitOpt.R1) &&  FitOpt.R1map)
     R1 = FitOpt.R1;
     R1f = R1 - kf*(R1r - R1) / (R1r - R1 + kf/F);
end

E1r = exp( -R1r * TR );
E1f = exp( -R1f * TR );
E2f = exp( -R2f * TR );

fw = exp( -W .* Trf );
fk = exp( -(kf+kr) * TR );

A = 1 + F - fw .* E1r .* ( F + fk );
B = 1 + fk .* ( F - fw .* E1r .* ( F + 1 ) );
C = F .* ( 1 - E1r ) .* ( 1 - fk );

My = M0f*sin(alpha) .* ((1-E1f).*B+C) ./ ( A - B.*E1f.*E2f - (B.*E1f-A.*E2f).*cos(alpha) );

end

