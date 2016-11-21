# Import libraries
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np
import os, os.path
import json
import sys

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
		if file != 'E-W-graphs2.py':
			with open('%s' % file, 'rb') as dump:
			    source = dump.read()
			    data = json.loads(source)

			# Create empty data stores for each country
			east_landfall = []
			west_landfall = []
			


			for item in data:
				start_lon = ((item[1])[2])[0]
				end_lon = ((item[1])[3])[0]
				if start_lon < end_lon:
					west_landfall.append((item[0])[1])
				else:
					east_landfall.append((item[0])[1])
			
			east_landfall.sort()
			e_bins = list(np.arange((round(east_landfall[0])-2),(round(east_landfall[-1])+2),1))
			plt.figure(1)
			plt.title('%s Number of Eastern Landfalls vs Latitude' % file)
			plt.hist(east_landfall,bins=e_bins)

			west_landfall.sort()
			w_bins = list(np.arange((round(west_landfall[0])-2),(round(west_landfall[-1])+2),1))
			plt.figure(2)
			plt.title('%s Number of Western Landfalls vs Latitude' % file)
			plt.hist(west_landfall,bins=w_bins)

			plt.show()
