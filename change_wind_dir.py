from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import itertools as IT
import re
import csv
import random

def columns(data):
	year = data[:, 0]
	month = data[:, 1]
	date = data[:, 2]
	hour = data[:, 3]
	sta_class = data[:, 4]
	wind_dir = data[:, 5]
	wind_sp = data[:, 6]
	temp = data[:, 7]
	mix_height = data[:, 8]
	preci_code = data[:, 9]
	preci_rate = data[:, 10]
	weight = data[:, 11]
	return year, month, date, hour, sta_class, wind_dir, wind_sp, \
	temp, mix_height, preci_code, preci_rate, weight
	'''
	clean(hour), clean(temp), \
	clean(wind_dir), clean(wind_sp), \
	list(map(lambda x: x*1.94384, clean(wind_sp))), \
	list(map(lambda x: x*3.28, clean(ceiling))), \
	clean(sky_cover_total), clean(humidity_rel), \
	list(map(lambda x: x*10, clean(preci_hourly)))
	'''
def main():
	data = np.genfromtxt('temp90.met', skip_header = 1)
	latti = 46.55 # site lattitude 
	year, month, date, hour, sta_class, wind_dir, wind_sp, \
	temp, mix_height, preci_code, preci_rate, weight = columns(data)
	# for i in range(len(wind_dir)):
	# 	wind_dir[i] += 180
	# 	if wind_dir[i] > 360:
	# 		wind_dir[i] -= 360
	f = open('temp_wind_dir.met', 'w')
	f.write('  0.200, 30.0   \n')
	for i in range(len(year)):
		f.write('{0:5d}{1:3d}{2:3d}{3:3d}{4:2d}{5:5d}.{6:6.1f} {7:.2f}{8:6d}.{9:2d}{10:7.2f}     1.\n'\
			.format(int(year[i]), int(month[i]), int(date[i]), int(hour[i]), int(sta_class[i]), \
				int(wind_dir[i]), wind_sp[i], temp[i], int(mix_height[i]), \
				int(preci_code[i]), preci_rate[i]))
	f.close()
	return

if __name__ == '__main__':
	main()