import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('code_validation_1000.csv')
x = []
LMSPD = []
FVM = []
x_COMSOL = []
COMSOL = []
x_exp = []
raw = []
for i in range(len(df['code x'])):
    x.append(df['code x'][i])
    LMSPD.append(df['LMSPD'][i])
    FVM.append(df['FVM'][i])
x.pop(0)
for i in range(len(x)):
    x[i] = float(x[i])
LMSPD.pop(0)
FVM.pop(0)
for i in range(1, 7):
    x_COMSOL.append(float(df['COMSOL x'][i]))
    COMSOL.append(float(df['COMSOL'][i]))
for i in range(1, 6):
    x_exp.append(float(df['exp x'][i]))
    raw.append(float(df['exp data'][i]))

plt.plot(x, LMSPD, 'k-')
plt.plot(x, FVM, 'b--')
plt.plot(x_COMSOL, COMSOL, 'r:')
plt.scatter(x_exp, raw, c = 'black')
plt.legend(['LMSPD', 'FVM', 'COMSOL', 'Experimental data'])
plt.title('code validation 1000C')
plt.xlabel('$p_1^{0.5}-p_2^{0.5}$ [atm$^{0.5}$]')
plt.ylabel('Permeation flux [mol/m-s$^2$]')
plt.show()