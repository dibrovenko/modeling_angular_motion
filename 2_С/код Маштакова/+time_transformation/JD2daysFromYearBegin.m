%	Version 1.0,
%	Author: Yaroslav Mashtakov
%   Developed by Keldysh Institute of Applied Mathematics of RAS
%   date: 20.07.2020
function [days_from_year_begin] = JD2daysFromYearBegin(julian_date_full)
%JD2DAYSFROMYEARBEGIN calculates amount of days passed from the beginning
%of the year
%   julian_date_full -- current julian date (1x1)

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


year = 100*b + d - 4800 + floor(m/10);
year_begin_JD = time_transformation.date2JD([year, 1, 1]);

days_from_year_begin = julian_date_full - year_begin_JD;


end

