#Import libraries
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np
import os, os.path
import json
import sys




# FUNCTIONS




# PARAMETER




# METHOD
# Define the relative path of the current working folder, which should be inside cyclone-data
REL_PATH = os.path.dirname(os.path.abspath(__file__))

# Create global data stores
g_latitude = []
g_vmax = []



# List all the files in the folder
filelist = os.listdir(REL_PATH)
for file in filelist:
	if file != '.DS_Store':
		if file != 'graphs.py':
			with open('%s' % file, 'rb') as dump:
			    source = dump.read()
			    data = json.loads(source)

			# Create empty data stores for each country
			latitude = []
			vmax = []
			
			for item in data:
				latitude.append((item[0])[1])
				vmax.append(((item[1])[2])[2])
				g_latitude.append((item[0])[1])
				g_vmax.append(((item[1])[2])[2])
				
			# # Create bins with size of 1 latitude 
			# bins = np.arange(0,70,1)

			# # Put bins index for each item
			# inds = np.digitize(latitude,bins)
			# l_inds = inds.tolist()

			# # Find the list of available bins
			# bins_available = []
			# for item in l_inds:
			# 	if (item in bins_available) == False:
			# 		bins_available.append(item)
			
			# for item in bins_available:
			# 	print item
			# 	# Create list to store all vmaxs in the bin
			# 	vmaxs = []
				

			# 	for item2 in inds:
			# 		if item2 == item:
			# 			print l_inds.index(item2)
			# 			vmaxs.append(vmax[l_inds.index(item2)])

			# 	print vmaxs

			
			latitude.sort()
			histogram_bins = list(np.arange((round(latitude[0])-2),(round(latitude[-1])+2),1))
			plt.figure()
			plt.title('%s Number of Landfalls vs Latitude' % file)
			plt.hist(latitude,bins=histogram_bins)
			plt.show()

# Create bins with size of 1 latitude 
bins = np.arange(0,50,1)

# Put bins index for each item
inds = np.digitize(g_latitude,bins)
l_inds = inds.tolist()


# Find the list of available bins
bins_available = []
for item in l_inds:
	if (item in bins_available) == False:
		bins_available.append(item)

bins_available.sort()

y =[]

for item in bins_available:
	
	# Create list to store all vmaxs in the bin
	vmaxs = []

	i = 0
	while i < len(l_inds):
		if l_inds[i] == item:
			vmaxs.append(g_vmax[i])
		i+=1
	y.append((sum(vmaxs)/len(vmaxs)))



# plt.figure(1)
# plt.title('Mean of Maximum Wind Speed vs Latitude')
# plt.xlabel('Latitude / degree')
# plt.ylabel('Mean of Maximum Windspeed / knots')
# plt.bar(bins_available,y)

# plt.figure(2)
# histogram_bins = list(np.arange(0,50,1))
# plt.title('Number of Landfalls vs Latitude')
# plt.xlabel('Latitude / degree')
# plt.ylabel('Number of Landfalls')
# plt.hist(g_latitude,bins=histogram_bins)



plt.show()

