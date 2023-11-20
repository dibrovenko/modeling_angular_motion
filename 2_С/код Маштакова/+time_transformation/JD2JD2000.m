function [JD2000] = JD2JD2000(JD)
%JD2JD2000 calculates amount of days from Julian date of 2000, 1 January 12:00 
%   JD -- current julian date 
JD2000 = JD - 2451545.0;
end

