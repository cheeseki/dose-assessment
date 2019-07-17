hanford = csvread('hanford_2020_110m.csv');
inl = csvread('inl_2020_110m.csv');
ornl = csvread('ornl_2020_110m.csv');

% hanford_GP =  fitrgp(hanford(:,1:3), hanford(:,4),'KernelFunction','matern52',...
%     'FitMethod','exact','PredictMethod','exact','Standardize',1,...
%     'OptimizeHyperparameters','all','HyperparameterOptimizationOptions',...
%     struct('MaxObjectiveEvaluations',25, 'KFold',5));
% 
% ornl_GP =  fitrgp(ornl(:,1:3), ornl(:,4),'KernelFunction','matern52',...
%     'FitMethod','exact','PredictMethod','exact','Standardize',1,...
%     'OptimizeHyperparameters','all','HyperparameterOptimizationOptions',...
%     struct('MaxObjectiveEvaluations',25, 'KFold',5));
% 
% inl_GP =  fitrgp(inl(:,1:3), inl(:,4),'KernelFunction','matern52',...
%     'FitMethod','exact','PredictMethod','exact','Standardize',1,...
%     'OptimizeHyperparameters','all','HyperparameterOptimizationOptions',...
%     struct('MaxObjectiveEvaluations',25, 'KFold',5));

load GP_surrogates.mat

hanford_T = 10.822 + rand(1e5,1)*(13.028 - 10.822);
hanford_W = normrnd(2.696, 0.274, [1e5,1]);
hanford_H = normrnd(60.726, 2.737, [1e5,1]);
dose_hanford = predict(hanford_GP,[hanford_T, hanford_W, hanford_H]);

inl_T = 8.494 + rand(1e5,1)*(9.535 - 8.494);
inl_W = normrnd(4.537, 0.4086, [1e5,1]);
inl_H = normrnd(57.69, 3.0895, [1e5,1]);
dose_inl = predict(inl_GP,[inl_T, inl_W, inl_H]);

ornl_T = 15.437 + rand(1e5,1)*(17.059 - 15.437);
ornl_W = normrnd(3.1289, 0.30534, [1e5,1]);
ornl_H = normrnd(71.53, 2.303, [1e5,1]);
dose_ornl = predict(ornl_GP,[ornl_T, ornl_W, ornl_H]);

figure()
hist(dose_hanford,50);
hold off

figure()
hist(dose_inl,50);
hold off

figure()
hist(dose_ornl,50);
hold off
