%	Version 1.0,
%	Author: Yaroslav Mashtakov
%   Developed by Keldysh Institute of Applied Mathematics of RAS
%   date: 20.07.2020

function [year] = JD2year(julian_date_full)
%JD2YEAR calculates current year from julian date
%   julian_date_full -- current julian date

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

end

