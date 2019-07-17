from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import itertools as IT
import re
import csv
import random

def load_data(filename):
	i = 0
	data = []
	day_summary = []
	with open(filename, 'r') as f:
		for line in f:
			if i%25 != 0:
				data.append(line.split())
			else:
				day_summary.append(line.split())
			i += 1
	data = np.asarray(data, dtype = 'object')
	# day_summary = np.array(day_summary, dtype = 'object')
	return data, day_summary

def columns(data):
	date = data[:, 0]
	hour = data[:, 1]
	Ra = data[:, 2]
	Ra_normal = data[:, 3]
	Rs = data[:, 4]
	Rs_normal = data[:, 5]
	Ra_diffuse = data[:, 6]
	sky_cover_total = data[:, 7]
	sky_cover_opaque = data[:, 8]
	temp = data[:, 9]
	dew = data[:, 10]
	humidity_rel = data[:, 11]
	pres = data[:, 12]
	wind_dir = data[:, 13]
	wind_sp = data[:, 14]
	vis = data[:, 15]
	ceiling = data[:, 16]
	obser = data[:, 17]
	weather_pre = data[:, 18]
	preci = data[:, 19]
	aerosol = data[:, 20]
	snow_depth = data[:, 21]
	snow_interval = data[:, 22]
	preci_hourly = data[:, 23]
	# eto = data[:, 24]
	# ep = data[:, 25]
	return date, clean(hour), clean(temp), \
	clean(wind_dir), clean(wind_sp), \
	list(map(lambda x: x*1.94384, clean(wind_sp))), \
	list(map(lambda x: x*3.28, clean(ceiling))), \
	clean(sky_cover_total), clean(humidity_rel), \
	list(map(lambda x: x*10, clean(preci_hourly)))

def clean(parameter):
	new = []
	for entry in parameter:
		new.append(float(re.sub("[AESTUZ]", "", entry)))
	parameter = new
	return parameter

def net_radiation_index(cloud_cover, ceiling, hour, solar, preci):
	if preci < 0:
		preci = 0
	if cloud_cover == 10 and ceiling <= 7000:
		net_ra = 0
	# night time assumed as 18-6
	elif hour < 6 or hour > 18:
		if preci > 0:
			net_ra = 0
		elif cloud_cover < 4:
			net_ra = -2
		else:
			net_ra = -1
	# daytime 
	else:
		# solar angle
		if solar <= 15:
			net_ra = 1
		elif solar <= 35:
			net_ra = 2
		elif solar <= 60:
			net_ra = 3
		else:
			net_ra = 4
		# modification
		if cloud_cover > 5 and preci == 0:
			if ceiling <= 7000:
				net_ra -= 2
			elif ceiling <= 16000:
				net_ra -= 1
			
			if cloud_cover == 10:
				net_ra -= 1

			if net_ra < 1:
				net_ra = 1

		elif preci > 0:
			net_ra -= 2
			if net_ra < 0:
				net_ra = 0
	return net_ra

def solar_angle(latti, hour, day):
# calculate solar angle
	decli_angle = -23.5*np.cos(np.pi*day/173)
	h_a = 180-hour/12*180
	solar = np.arcsin(np.sin(latti)*np.sin(decli_angle)+np.cos(latti)*np.cos(decli_angle)*np.cos(h_a))
	return solar

def stability(net_ra, wind_sp):
# calculate stability class
	# print(net_ra, wind_sp)
	if net_ra == 4:
		if wind_sp < 5.5: # knots 
			sta_class = 1
		elif wind_sp < 9.5:
			sta_class = 2
		else:
			sta_class = 3
	elif net_ra == 3:
		if wind_sp < 1.5: # knots 
			sta_class = 1
		elif wind_sp < 7.5:
			sta_class = 2
		elif wind_sp < 11.5:
			sta_class = 3
		else:
			sta_class = 4
	elif net_ra == 2:
		if wind_sp < 3.5: # knots 
			sta_class = 2
		elif wind_sp < 9.5:
			sta_class = 3
		else:
			sta_class = 4
	elif net_ra == 1:
		if wind_sp < 3.5: # knots 
			sta_class = 3
		else:
			sta_class = 4
	elif net_ra == 0:
		sta_class = 4
	elif net_ra == -1:
		if wind_sp < 3.5: # knots 
			sta_class = 6
		elif wind_sp < 6.5:
			sta_class = 5
		else:
			sta_class = 4
	elif net_ra == -2:
		if wind_sp < 3.5: # knots 
			sta_class = 7
		elif wind_sp < 6.5:
			sta_class = 6
		elif wind_sp < 10.5:
			sta_class = 5
		else:
			sta_class = 4
	return sta_class

def plot(dictionary):
	for key, values in dictionary.items():
		plt.plot(values)
		plt.title('{0}'.format(key))
		plt.show()
	return

def variation(parameter):
	year_average = np.average(parameter)
	maximum = np.amax(parameter)
	minimum = np.amin(parameter)
	day_average = []
	for i in range(int(len(parameter)/24)): # number of days
		day_data = parameter[(i*24):((i+1)*24)]
		# print(day_data)
		day_average.append(np.average(day_data))
	return day_average, year_average, maximum, minimum

def change_temp(dry_bulb, RH):
	a = 6.1121 # mb
	b = 18.678 
	c = 257.14 # degC
	d = 234.5 # degC
	dew_point = []
	for i in range(len(dry_bulb)):
		gamma = np.log(RH[i]/100)+b*dry_bulb[i]/(c+dry_bulb[i])
		dew_point.append(c*gamma/(b-gamma))
	return dew_point


def write_met_windsp(data, day_summary, wind_sp, LHS_sample, j):
	for i in range(len(wind_sp)):
		wind_sp[i] = wind_sp[i]*LHS_sample
	with open('pred{0}.h90'.format(j), 'w') as f:
		for i in range(len(data)+len(day_summary)):
			if i == 0:
				f.write(' 24243 Yakima                         WA  +8  N  46 34  W 120 32   324   2002-07-02 16:28:53\n')
			elif i%25 == 0:
				j = int(np.floor(i/25))
				k = day_summary[j]
				f.write('{0:>11s}{1:>3s}{2:>7s}{3:>7s}{4:>7s}  {5:>7s}  {6:>7s}  {7:>4s}{8:>4s}{9:>7s}{10:>7s}{11:>5s}{12:>7s}{13:>5s}{14:>7s}{15:>8s}{16:>8s}{17:>3s}{18:>11s}{19:>5s}{20:>8s}{21:>6s}{22:>5s}{23:>8s}{24:>9s}{25:>8s}\n'\
					.format(k[0], k[1], k[2], k[3], k[4], k[5], k[6], k[7], k[8], k[9], \
						k[10], k[11], k[12], k[13], k[14], k[15], k[16], k[17], k[18], k[19], \
						k[20], k[21], k[22], k[23], k[24], k[25]))
			else:
				j = int(i-1-np.floor(i/25))
				k = data[j]
				k[14] = wind_sp[j]
				f.write('{0:>11s}{1:>3s}{2:>7s}{3:>7s}{4:>9s}{5:>9s}{6:>9s}{7:>4s}{8:>4s}{9:>7s}{10:>7s}{11:>5s}{12:>7s}{13:>5s}{14:>6.1f}S{15:>8s}{16:>8s}{17:>3s}{18:>11s}{19:>5s}{20:>8s}{21:>6s}{22:>5s}{23:>8s}\n'\
					.format(k[0], k[1], k[2], k[3], k[4], k[5], k[6], k[7], k[8], k[9], \
						k[10], k[11], k[12], k[13], k[14], k[15], k[16], k[17], k[18], k[19], \
						k[20], k[21], k[22], k[23]))
	return

def main():

	latti = 46.55 # site lattitude 
	# data, day_summary = load_data('{0}pred_T.h90'.format(j))
	data, day_summary = load_data('pred0.h90')
	# precipitation rate [mm/hr]
	date, hour, temp, wind_dir, wind_sp, wind_sp_knot, \
	ceiling, sky_cover_total, humidity_rel, preci = columns(data)
	solar = []
	net_ra = []
	sta_class = []
	for i in range(len(temp)):
		solar.append(solar_angle(latti, hour[i], i+1))
		net_ra.append(net_radiation_index(sky_cover_total[i], ceiling[i], hour[i], solar[i], preci[i]))
		sta_class.append(stability(net_ra[i], wind_sp_knot[i]))
		i += 1
		dictionary = {
	            "temperature": temp,
	            "temp_day_average": variation(temp),
	            "wind speed": wind_sp, 
	            "wind_sp_day_average": variation(wind_sp),
	            "humidity_relative": humidity_rel,
	            "humidity_rel_day_average": variation(humidity_rel),
	            "hourly precipitation": preci,
	            "stability class": sta_class
	            }
	
	plt.scatter(preci, wind_sp)
	plt.show()
	# change wind speed
	# write_met_windsp(data, day_summary, wind_sp, LHS_wsp[j], j)
	return

if __name__ == '__main__':
	main()