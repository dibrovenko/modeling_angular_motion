%	Version 1.1,
%	Author: Yaroslav Mashtakov
%   Developed by Keldysh Institute of Applied Mathematics of RAS
%   date: 21.03.2023
function [ norm_mat ] = normComputeGrav(N)
%NORM_COMPUTE calculates normalizing coefficients for gravity field NxN (10x10 by default)
if nargin == 0
    N = 10;
end
norm_mat = ones(N + 1, N + 1); 

for k = 1:N
    for m = 0:k
        tmp1 = 1;
        for i = (k - m + 1):(k + m)
            tmp1 = tmp1*i;
        end
        tmp1 = tmp1/(2*k + 1);
        if m == 0
            norm_mat(k + 1, m + 1) = sqrt(tmp1);
        else
            norm_mat(k + 1, m + 1) = sqrt(tmp1/2);
        end
    end
end
end

