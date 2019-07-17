function dose_ornl = dose_ornl(theta)
load GP_surrogates.mat
dose_ornl = predict(ornl_GP, theta);