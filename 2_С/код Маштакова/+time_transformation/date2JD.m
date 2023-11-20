%	Version 1.0,
%	Author: Yaroslav Mashtakov
%   Developed by Keldysh Institute of Applied Mathematics of RAS
%   date: 20.07.2020
function [JD] = date2JD(date_vec)
%DATE2JD calculates julian date from date
% date_vec -- vector. Might have different size: from 1x3 (year, month,
% day) to 1x6 (year, month, day, hour, minute, second)


if ~isvector(date_vec) || length(date_vec) < 3 || length(date_vec) > 6
    error('Input must be a vector. Its length might be equal to 3, 4, 5 or 6')
end

days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]; % amount of days in corresponding months
JULDAY_CONST = 1721422.5;

% year to days
year = date_vec(1) - 1;
A = floor(year/100);
B = 2 - A + floor(A/4);
days = floor(365.25*year) + JULDAY_CONST + B;

% months to days
for i = 1:date_vec(2) - 1
    days = days + days_in_months(i);
end
if (mod(date_vec(1), 4) == 0) && (mod(date_vec(1), 100) ~= 0 || mod(date_vec(1), 400) == 0) && date_vec(2) > 2 % check for leap year
    days = days + 1;
end

% add days
days = days + date_vec(3);

% calculate hours, minutes, seconds
conversion_const = [1/24, 1/1440, 1/86400]; % hours, minutes, seconds
addit_day = 0;
for i = 4:length(date_vec)
    addit_day = addit_day + date_vec(i)*conversion_const(i - 3);
end

JD = days + addit_day;

end

