function [MJD] = JD2MJD(JD)
%JD2MJD calculates modified julian date from julian date
%   JD -- current julian date
MJD = JD - 2400000.5;
end

