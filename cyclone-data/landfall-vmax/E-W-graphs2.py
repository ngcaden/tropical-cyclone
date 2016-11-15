# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import os, os.path
import json
import sys

# METHOD
# Define the relative path of the current working folder, which should be inside cyclone-data
REL_PATH = os.path.dirname(os.path.abspath(__file__))

# Define countries that are deemed West or East
East = ['Japan']
West = ['Vietnam']



# List all the files in the folder
filelist = os.listdir(REL_PATH)

for country in West:
	with open('%s' % country, 'rb') as dump:
	    source = dump.read()
	    data = json.loads(source)

	landfall_latitude = [item[0] for item in data]
	plt.figure(1)
	plt.title('%s Number of Landfalls vs Latitude' % country)
	bins = np.arange(0,50,1)

	plt.hist(landfall_latitude, bins=bins)

	
	# print landfall_latitude
	# # Put bins index for each item
	# inds = np.digitize(landfall_latitude,bins)

	# # Find the list of available bins
	# bins_available = []
	# for item in inds:
	# 	if (item in bins_available) == False:
	# 		bins_available.append(item)
	# print 
	# bins_available.sort()

	# y =[]

	# for item in bins_available:
	# 	# Create list to store all vmaxs in the bin
	# 	vmaxs = []

	# 	for item1 in landfall_latitude:
	# 		if inds[landfall_latitude.index(item1)] == item:
	# 			vmaxs.append((data[landfall_latitude.index(item1)])[2])
	# 	print vmaxs
	# 	y.append((sum(vmaxs)/len(vmaxs)))

	# plt.figure(2)
	# plt.title('%s Mean of Maximum Wind Speed vs Latitude' % country)
	# plt.xlabel('Latitude / degree')
	# plt.ylabel('Mean of Maximum Windspeed / knots')
	# plt.bar(bins_available,y)

	plt.show()
