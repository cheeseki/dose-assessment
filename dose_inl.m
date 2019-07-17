function dose_inl = dose_inl(theta)
load GP_surrogates.mat
dose_inl = predict(inl_GP, theta);