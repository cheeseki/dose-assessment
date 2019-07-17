import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('solubility.csv')
df.columns = ['temperature', 'Gevantman', 'Engineering toolbox']
T = []
S1 = []
S2 = []
for i in range(len(df['temperature'])):
    T.append((df['temperature'][i]))
    S1.append((df['Gevantman'][i]))
    S2.append((df['Engineering toolbox'][i]))
T.pop(0)
S1.pop(0)
S2.pop(0)
for i in range(len(T)):
    T[i] = float(T[i])
    S1[i] = float(S1[i])
    S2[i] = float(S2[i])

plt.plot(T, S1, 'k-')
plt.plot(T, S2, 'b--')
plt.legend(['Gevantman', 'Engineering toolbox'])
plt.title('solubility of H2 in water')
plt.xlabel('Temperature [°C]')
plt.ylabel('H$_2$ solubility in water [mol/m$^3$]')
plt.show()