function dose_hanford = dose_hanford(theta)
load GP_surrogates.mat
dose_hanford = predict(hanford_GP, theta);