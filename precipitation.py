import numpy as np
import csv

y = 100
u_avg = 5 # mean wind speed
# sigma_y = 
# sigma_z = # plum-rise parameters
F = 1 # fractional delpletion of plume
h = 30 # effective height of release [m]

properties = np.genfromtxt('overall_mass_transfer_coeff.csv', skip_header = 4, delimiter = ',') # overall mass tansfer coeff.
K_y_HT_glc = (properties[:, 1]*10000) # mol/m^2-s
K_y_HTO_glc = (properties[:, 2]*10000) # mol/m^2-s
K_y_HT_sd = (properties[:, 3]*10000) # mol/m^2-s
K_y_HTO_sd = (properties[:, 4]*10000) # mol/m^2-s
a = (properties[:, 0]/100) # drop size [m]

# v_t = # terminal velocity
E = 1.02 # capture efficiency
# m = # liquid water conent of fog 
rho_w = 1000 # wate density, kg/m3
M_w = 0.018 # water molecular weight, kg/mol
diff_coeff = np.genfromtxt('diff_coeff.csv', delimiter = ',')
T = diff_coeff[:, 0]
H = (diff_coeff[:, 5]/10000) # HTO diff coeff in water, m^2/s
H_prim = H*M_w/rho_w # Henry's constant 

# k = -(3*E*m)/(4*a*H_prim*rho_w)+(3*K_y)/(v_t*a)
# p = 3*K_y*H_prim/(v_t*a)

# c_Ao = -Q*F*k/(2*sqrt(2*np.pi)*sigma_y*u_avg)*...
# exp(-y*y/(2*sigma_y*sigma_y)+sigma_z*sigma_z*p*p/2)*...
# (exp(p*h)*(1-erf((-sigma_z*sigma_z*p-h)/(sigma_z*sqrt(2))))+...
# 	exp(-p*h)*(1-erf((-sigma_z*sigma_z*p+h)/(sigma_z*sqrt(2))))