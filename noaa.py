from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import itertools as IT
import re
import csv

def load_data(filename):
	data = np.loadtxt(filename, delimiter = ',', skiprows = 2,
		usecols = np.r_[range(6, 22)], dtype=str)
	# print(data[0, :])
	date = data[:, 0]
	year = np.zeros(len(date))
	month = np.zeros(len(date))
	day = np.zeros(len(date))
	sky_cover_total = data[:, 1]
	sky_cover_day = data[:, 2]
	wind_sp = data[:, 3]
	preci = data[:, 9]
	temp = data[:, 13]
	temp_max = data[:, 14]
	temp_min = data[:, 15]
	for i in range(len(date)):
		if sky_cover_total[i] == '':
			sky_cover_total[i] = 0
		if sky_cover_day[i] == '':
			sky_cover_day[i] = 0
		if wind_sp[i] == '':
			wind_sp[i] = 0
		if preci[i] == '':
			preci == 0
		if temp_max[i] == '':
			temp_max[i] = 0
		if temp_min[i] == '':
			temp_min[i] = 0
		month[i], day[i], year[i] = date[i].split('/')
	return year.astype(int), month.astype(int), day.astype(int), \
	wind_sp.astype(float), temp.astype(float), \
	temp_min.astype(float), temp_max.astype(float)

def boundary(parameter):
	return max(parameter), min(parameter)

def year_avg(year, year_range, parameter):
	avg = []
	single_year = {}
	for i in range(len(year_range)):
		year_list = []
		for j in range(len(year)):
			if year_range[i] == year[j]:
				year_list.append(parameter[j])
		single_year[year_range[i]] = year_list
		avg.append(np.average(year_list))
	return avg, single_year

def main():
	year, month, day, wind_sp, temp, temp_min, temp_max = load_data('1479826.csv')
	maxtemp, _ = boundary(temp_max)
	_, mintemp = boundary(temp_min)
	maxwind_sp, minwind_sp = boundary(wind_sp)
	year_range = [90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 00,
	1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
	11, 12, 13, 14, 15, 16, 17]
	avg_temp, single_year_temp = year_avg(year, year_range, temp)
	avg_wind, single_year_wind = year_avg(year, year_range, wind_sp)
	with open('recent_years_temp.csv', 'w') as f:
		[f.write('{0}, {1}\n'.format(key, values)) for key, values in single_year_temp.items()]
	with open('recent_years_wind.csv', 'w') as f:
		[f.write('{0}, {1}\n'.format(key, values)) for key, values in single_year_wind.items()]
	
	# plt.plot(avg)
	# plt.show()
	return

if __name__ == '__main__':
	main()