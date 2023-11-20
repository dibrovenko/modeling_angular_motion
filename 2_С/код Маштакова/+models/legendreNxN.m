%	Version 1.1,
%	Author: Yaroslav Mashtakov
%   Developed by Keldysh Institute of Applied Mathematics of RAS
%   date: 21.03.2023
function [ a ] = legendreNxN( cfi, sfi, N)
%LEGENDRE10X10 calculates legendre polinomials
%   cfi -- cosine  [1x1]
%   sfi -- sine    [1x1]

a = zeros(N + 1, N + 2);
a(1, 1) = 1;
a(2, 1) = sfi;
a(2, 2) = cfi;
for k = 3:N + 1
    a(k, 1) = ((2*k-3)*sfi*a(k - 1, 1) - (k - 2)*a(k - 2, 1))/(k - 1);
    a(k, k) = (2*k-3)*cfi*a(k - 1, k - 1);
    for m = 2:k + 1
        a(k, m) = a(k - 2, m) + (2*k - 3)*cfi*a(k - 1, m - 1);
    end
end

end

