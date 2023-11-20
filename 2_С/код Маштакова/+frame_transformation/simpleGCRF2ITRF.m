%	Version 1.0,
%	Author: Yaroslav Mashtakov
%   Developed by Keldysh Institute of Applied Mathematics of RAS
%   date: 20.07.2020
function [gcrf2itrf_DCM] = simpleGCRF2ITRF(t_jd)
% returns direction cosine matrix from Geocentric Celestial Reference Frame 
% to International Terrestrial Reference Frame. Expression is simplified,
% does not take into account precession and nutation
%   t_jd -- current time in julian days (1x1)

DJ00 = 2451545.0;

t_jd_from_J2000 = (t_jd - DJ00); % days from J2000

% see vallado, 4th edition, p.213
theta = 2*pi*(0.7790572732640 + 1.00273781191135448 *t_jd_from_J2000);

gcrf2itrf_DCM = [cos(theta), sin(theta), 0;
               -sin(theta), cos(theta), 0;
                     0,         0,      1];

end
