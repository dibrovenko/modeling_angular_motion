clc
clear all
close all

start_date = [2023 7 11 12 0 0];
start_date_JD = time_transformation.date2JD(start_date); % transform to Julian Days
ITRF2GCRF = frame_transformation.simpleGCRF2ITRF(start_date_JD); % now we get transition matrix from ITRF to GCRF (inertial frame to greenwich frame)

