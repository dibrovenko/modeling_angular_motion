clc
clear all
close all
% everything must be in meters, seconds, kilos!

mu_earth = 398600.4415e9; % earth gravity parameter
earth_radius = 6371.302e3; 
root_path = pwd; % path to the current folder
N_harmonics = 10;  % amount of harmonics
model = 'EGM2008'; % model of ravity. Either EGM2008 or EGM96
[koefsC, koefsS, norm_coefs_grav] = models.loadCoefsGravNxN(root_path, N_harmonics, model);

r_GCRF = [6400e3; 0; 0]; % radius vector in greenwich frame 
grav_acceleration = -mu_earth*r_GCRF/norm(r_GCRF)^3; % gravity from central field
grav_acceleration = grav_acceleration ...
                  + models.getGravNxN(r_GCRF,... % additional acceleration caused by higher harmonics
                                      koefsC,...
                                      koefsS,...
                                      norm_coefs_grav,...
                                      earth_radius,...
                                      mu_earth,...
                                      N_harmonics);
% NB: grav acceleration is given in greenwich frame, not inertial one! We
% need to multiply it by transition matrix to get values in inertial frame