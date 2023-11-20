%	Version 1.0,
%	Author: Yaroslav Mashtakov
%   Developed by Keldysh Institute of Applied Mathematics of RAS
%   date: 20.07.2020
function [ koefsC, koefsS, norm_coefs_grav ] = loadCoefsGravNxN(root_path, N, model)
%loadKoefsGrav10x10 loads coefficients for gravity field 10x10
%   root_path -- path to the folder with modeller
switch model
    case 'EGM96'
        path = [root_path, '/+models/field_constants/EGM96.txt'];
    case 'EGM2008'
        path = [root_path, '/+models/field_constants/EGM2008_to2190_TideFree_180.txt']; 
    otherwise
        error('unknown gravity model. Must be either EGM96 or EGM2008')
end
tmp = load(path);
koefsC = zeros(N + 1, N + 1);
koefsS = zeros(N + 1, N + 1);
norm_coefs_grav = models.normComputeGrav(N);
for i = 1:length(tmp)
    if tmp(i, 1) > N
        break;
    end
    koefsC(tmp(i, 1) + 1, tmp(i, 2) + 1) = tmp(i, 3);
    koefsS(tmp(i, 1) + 1, tmp(i, 2) + 1) = tmp(i, 4);
end
end

