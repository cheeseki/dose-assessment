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
	LHS_wsp = [0.702196949, 0.797345616, 0.799393257, 0.818852019, 0.733081286, 0.757129555, 0.740641776, \
	0.682300057, 0.679752482, 0.790468512, 0.737800953, 0.964953276, 0.825373034, 0.797932867, 0.823356475, \
	0.933647114, 0.764326099, 0.896537429, 0.881493846, 0.855096385, 0.644490812, 0.747785152, 0.728371452, \
	0.809065314, 0.689327083, 0.753076147, 0.866987074, 0.724965754, 0.622185518, 0.997817455, 0.804625284, \
	0.722450914, 0.767514008, 0.831207138, 0.795283947, 0.769855504, 0.802349715, 0.707202646, 0.847421998, \
	0.850564801, 0.780627251, 0.834168779, 0.758765349, 0.828692232, 0.698743496, 0.78428149, 0.814239895, \
	0.695466657, 0.664719046, 0.743111707, 0.771063794, 0.836849087, 0.686420438, 0.890005322, 0.718203575, \
	0.756214066, 0.762354489, 0.921124353, 0.705039775, 0.876271537, 0.791374286, 0.739227836, 0.884075041, \
	0.78826593, 0.772085483, 0.845731722, 0.750494962, 0.915385521, 0.793123133, 0.838562406, 0.81571178, \
	0.713184742, 0.85210692, 0.869988344, 0.636702177, 0.806184225, 0.725754191, 0.832832006, 0.78135414, \
	0.839597199, 0.787703573, 0.800854666, 0.714683138, 0.751818225, 0.731216711, 0.862275636, 0.928232243, \
	0.808056391, 0.877553142, 0.940941494, 0.811479075, 0.841190463, 0.760882565, 0.776501414, 0.671292848, \
	0.844207141, 0.744261513, 0.858974777, 0.952955185, 0.778667542, 0.746036921, 0.649678476, 0.899674467, \
	0.821454482, 0.765118113, 0.907548866, 0.826876695, 0.812399255, 0.785003885, 0.873358363, 0.658223329, \
	0.776385284, 0.735083099, 0.709068426, 0.694214397, 0.886138852, 0.675136868, 0.903892859, 0.820336552, \
	0.615110561, 0.579430497, 0.864905612, 0.774623987, 0.8571112, 0.720522715]
	latti = 46.55 # site lattitude 
	for j in range(125):
		data, day_summary = load_data('{0}pred_T.h90'.format(j))
		# data, day_summary = load_data('w24243.h90')
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
		
		# change wind speed
		write_met_windsp(data, day_summary, wind_sp, LHS_wsp[j], j)
	return

if __name__ == '__main__':
	main()