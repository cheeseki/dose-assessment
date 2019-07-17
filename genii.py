import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 16})
import pandas as pd
import matplotlib.mlab as mlab
import scipy.stats as stats
import numpy as np

df = pd.read_csv('C:\\Users\\xwunuke\\Desktop\\T_try\\Hanford\\temp.csv')
df.columns = ['x1', 'hanford','inl',  'ornl']
x1 = []
# x2 = []
# x3 = []
hanford = []
inl = []
ornl = []

for i in range(len(df['x1'])):
    x1.append(float(df['x1'][i]))
    hanford.append(float(df['hanford'][i])*10)
# for i in range(len(df['x2'])):
#     x2.append(float(df['x2'][i]))
    inl.append(float(df['inl'][i])*10)
# for i in range(len(df['x3'])):
#     x3.append(float(df['x3'][i]))
    ornl.append(float(df['ornl'][i])*10)

plt.plot(x1, hanford, 'k-')
plt.plot(x1, inl, 'b--')
plt.plot(x1, ornl, 'r:')
plt.scatter(1.536917808,0.50661075, c='k')
plt.scatter(-0.126175799,0.65887382, c='b')
plt.scatter(-0.392212329,0.59860779, c='r')
plt.legend(['Hanford', 'Idaho Falls', 'Oak Ridge', 'Hanford mean', 'Idaho Falls mean', 'Oak Ridge mean'], loc = 'center left', bbox_to_anchor = (1,0.5))
# plt.title('Effect of wind speed on dosimetry')
plt.xlabel('Relative temperature [°C]')
plt.ylabel('Max. individual dose [mSv]')
# plt.xticks(np.arange(60, 220, step=20))
plt.show()


#
# df = pd.read_csv('C:\\Users\\xwunuke\\Desktop\\T_try\\ORNL\\historical_temp_ornl.csv')
# df.columns = ['x1', 'temp']
# x1 = []
# j = []
# temp = []
# maximum = []
# minimum = []
# for i in range(len(df['x1'])):
#     x1.append(float(df['x1'][i]))
#     temp.append(float(df['temp'][i]))
#
# for i in range(1990, 2022):
#     j.append(i)
#     maximum.append(0.0215*i-26.371)
#     minimum.append(0.0343*i-53.849)
#
# plt.scatter(x1, temp)
# plt.plot(j, maximum, 'r--')
# plt.plot(j, minimum, 'b:')
#
# # plt.legend(['Hanford', 'Idaho Falls', 'Oak Ridge'])
# # , loc = 'center left', bbox_to_anchor = (1,0.5))
# # plt.title('Oak Ridge annual average temperature')
# plt.xlabel('Year')
# plt.ylabel('Annual average temperature [°C]')
# plt.text(1973, 16.5, 'upper bound', fontsize=16)
# plt.text(2002, 14.6, 'lower bound', fontsize=16)
# plt.show()
#
# # plot historical wind speed/humidity
df = pd.read_csv('C:\\Users\\xwunuke\\Desktop\\T_try\\ORNL\\historical_wind_ornl.csv')
df.columns = ['x1', 'temp']
x1 = []
j = []
temp = []
maximum = []
minimum = []
for i in range(len(df['x1'])):
    x1.append(float(df['x1'][i]))
    temp.append(float(df['temp'][i]))

plt.scatter(x1, temp)
# plt.legend(['Hanford', 'Idaho Falls', 'Oak Ridge'])
# , loc = 'center left', bbox_to_anchor = (1,0.5))
# plt.title('Oak Ridge annual average humidity')
plt.xlabel('Year')
plt.ylabel('Annual average wind speed [m/s]')
plt.show()
#
# # plt.hist(temp, 20)
# density = stats.gaussian_kde(temp)
# n, x, _ = plt.hist(temp, 20,
#                    histtype=u'step', density=True)
# plt.plot(x, density(x), linewidth=2)
# plt.title('Oak Ridge annual average humidity histogram')
# plt.xlabel('Annual average relative humidity')
# plt.ylabel('Frequency')
# plt.show()
#
# startup time
x = [18500, 185000]
dose = [0.503, 5.03]
plt.plot(x, dose)
# plt.title('effect of startup time on dosimetry')
plt.xlabel('Daily tritium release rate [GBq/day]')
plt.ylabel('Max. individual dose [mSv]')
plt.xticks(np.arange(18500, 185001, step=33300))
plt.show()