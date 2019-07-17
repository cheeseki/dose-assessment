
%% 1 - INITIALIZE THE UQLAB FRAMEWORK AND CLEAR THE WORKSPACE
%  Clear variables from the workspace and reinitialize the UQLab framework
clearvars;
uqlab;

%% 2 - MODEL
%  COMPUTATIONAL MODEL
% Create a model object that uses the uq_SimplySupportedBeam9points function:
Model.mFile = 'dose_inl'; % specify the function name
myModel = uq_createModel(Model);               % create and add the model to UQLab

%% 3 - PROBABILISTIC INPUT MODEL

Input.Marginals(1).Name = 'T';
Input.Marginals(1).Type = 'Uniform';
Input.Marginals(1).Parameters = [8.494, 9.536]; % (m)

Input.Marginals(2).Name = 'wind';
Input.Marginals(2).Type = 'Gaussian';
Input.Marginals(2).Parameters = [4.537, 0.4086]; % (m)

Input.Marginals(3).Name = 'humidity';
Input.Marginals(3).Type = 'Gaussian';
Input.Marginals(3).Parameters = [57.69, 3.0895]; % (m)

myInput = uq_createInput(Input);
uq_display(myInput);
%% 4 - SENSITIVITY ANALYSIS
% Sensitivity analysis is performed by calculating the Sobol' indices for
% each of the output components separately.

SobolOpts.Type = 'Sensitivity';
SobolOpts.Method = 'Sobol';
% SobolOpts.Sampling = 'lhs';
SobolOpts.Sobol.Order = 1;
SobolOpts.Sobol.SampleSize = 1e5;
mySobolAnalysisMC = uq_createAnalysis(SobolOpts);
mySobolResultsMC = mySobolAnalysisMC.Results;


