%	Version 1.1,
%	Author: Yaroslav Mashtakov
%   Developed by Keldysh Institute of Applied Mathematics of RAS
%   date: 21.03.2023
function result_acceleration_GF = getGravNxN(position_GF, koefsC, koefsS, norm_coefs, earth_radius, mu_earth, N)
% Calculates gravity from the Earth gravity field, 10x10 harmonics. 
% Does not include cental field! position vector must be given in ITRF

% position_GF -- satellite position in ITRF [meters] (3x1) 
% koefsC -- koefficients for cosines
% koefsS -- koefficients for sines
% earth_radius -- [meters] (1x1)
% mu_earth -- earth gravitational parameter [m^3/s^2]  (1x1)
% N -- amount of harmonics
% altitude, latitude, longitude calculation
altitude = norm(position_GF);
latit = asin(position_GF(3)/altitude);
longi = atan2(position_GF(2), position_GF(1));
% 
% altitude = 7218.032973047451*1e3;
% latit = 10.4347768520963*pi/180;
% longi = 79.53818575398761*pi/180;

dUr = 0;
dUfi = 0;
dUl = 0;


ri = position_GF(1);
rj = position_GF(2);
rk = position_GF(3);
req = sqrt(position_GF(1)^2 + position_GF(2)^2);

legendre_mat =  models.legendreNxN(cos(latit), sin(latit), N);

tan_lat = tan(latit);
for k = N + 1:(-1):3
    for m = k:(-1):1
        P_km = legendre_mat(k, m)/norm_coefs(k, m);
        P_km_p_1 = legendre_mat(k, m + 1)/norm_coefs(k, m);
        dUr = dUr + (earth_radius/altitude)^(k - 1)*k*P_km*...
                    ( koefsC(k, m)*cos((m - 1)*longi) ...
                    + koefsS(k, m)*sin((m - 1)*longi));
        dUfi = dUfi + (earth_radius/altitude)^(k - 1)*...
                      (P_km_p_1 - (m - 1)*tan_lat*P_km)*... 
                      (koefsC(k, m)*cos((m - 1)*longi) + koefsS(k, m)*sin((m - 1)*longi));
        dUl = dUl + (earth_radius/altitude)^(k - 1)*(m - 1)*P_km*...
                    (koefsS(k, m)*cos((m - 1)*longi) - koefsC(k, m)*sin((m - 1)*longi));
    end
end

dUr = -dUr*(mu_earth/altitude^2);
dUfi = dUfi*(mu_earth/altitude);
dUl = dUl*(mu_earth/altitude);

result_acceleration_GF = zeros(3, 1);
result_acceleration_GF(1) = (dUr/altitude - dUfi*rk/req/altitude^2)*ri - dUl/req^2*rj;
result_acceleration_GF(2) = (dUr/altitude - dUfi*rk/req/altitude^2)*rj + dUl/req^2*ri;
result_acceleration_GF(3) = dUr/altitude*rk + dUfi/altitude^2*req;


end
