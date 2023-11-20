%	Version 1.0,
%	Author: Yaroslav Mashtakov
%   Developed by Keldysh Institute of Applied Mathematics of RAS
%   date: 20.07.2020
function [date_vec] = JD2date(julian_date_full)
% JD2date calculates date in the format 
% [year, month, day, hour, minute, second] from julian date
% julian_date_full -- current julian date (1x1)

if ~isequal(size(julian_date_full), [1, 1]) || ~isnumeric(julian_date_full)
    error('Input must be numerical array with a size 1x1')
end

JD = floor(julian_date_full + 0.5);

% magic numbers from russian wiki on julian date
a = JD + 32044;
b = floor((4*a + 3)/146097);
c = a - floor((146097*b)/4);
d = floor((4*c + 3)/1461);
e = c - floor(1461*d/4);
m = floor((5*e + 2)/153);

day = e - floor((153*m + 2)/5) + 1;
month = m + 3 - 12*floor(m/10);
year = 100*b + d - 4800 + floor(m/10);

% seconds from the beginning of the day
secs_from_day = (julian_date_full - (JD - 0.5))*86400;

hour = floor(secs_from_day/3600);

tmp = secs_from_day - hour*3600;

minutes = floor(tmp/60);

sec = tmp - minutes*60;

date_vec = [year month day hour minutes sec];

end