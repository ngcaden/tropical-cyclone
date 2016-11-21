# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import os, os.path
import json
import sys

# FUNCTIONS
# Progress bar for command line during runtime
def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  


# PARAMETER
binwidth = 0.1

# METHOD
# Define the relative path of the current working folder, which should be inside cyclone-data
REL_PATH = os.path.dirname(os.path.abspath(__file__))

# Define countries that are deemed West or East
# West = ['Vietnam','China','South-Korea']
West = ['China']

West_landfall = []
West_vmax = []

# List all the files in the folder
filelist = os.listdir(REL_PATH)

# Extract and plot for Western countries
for country in West:
	
	# Load the data of the country
	with open('%s' % country, 'rb') as dump:
	    source = dump.read()
	    data = json.loads(source)

	# Extract landfall latitude and vmax 
	landfall_latitude = [round(item[0]*10)/10. for item in data]
	landfall_vmax = [item[1] for item in data]
	
	# Add the data to Eastern database
	West_landfall.extend(landfall_latitude)
	West_vmax.extend(landfall_vmax)

	# Create a bins for all the latitudes recorded
	bins = np.arange(min(landfall_latitude), 
			max(landfall_latitude) + binwidth, binwidth)


	# Plot a histogram of landfall latitude 
	plt.figure()
	plt.title('%s Number of Landfalls vs Latitude' % country)
	plt.xlabel('Latitude')
	plt.ylabel('Counts')
	plt.hist(landfall_latitude, bins=bins)
	
	# Put bins index for latitude
	inds = np.digitize(landfall_latitude,bins)

	# Create a list for mean vmaxs
	mean_vmax =[]

	bin_number = 0
	while bin_number < len(bins):
		# Create list to store all vmaxs in the bin
		vmaxs = []

		latitude_number = 0

		while latitude_number < len(landfall_latitude):
			# Check for points in the bins
			if inds[latitude_number] == bin_number:
				# If the point is in the bin, add vmax to list vmaxs
				vmaxs.append(landfall_vmax[latitude_number])
			latitude_number += 1

		# If no point exist, add 0 to list mean vmax
		if len(vmaxs) == 0:
			mean_vmax.append(0)

		# If not, calculate and add the mean
		else:		
			mean_vmax.append(sum(vmaxs)/len(vmaxs))
		bin_number += 1
		progress(bin_number,len(bins))

	# Plot mean vmax against latitude
	plt.figure()
	plt.title('%s Mean of Maximum Wind Speed vs Latitude' % country)
	plt.xlabel('Latitude / degree')
	plt.ylabel('Mean of Maximum Windspeed at Landfall / knots')
	plt.bar(bins,mean_vmax,width=0.1)





# GLOBAL

# Plot for Western Region

# Create bins of all recorded latitude
bins = np.arange(min(West_landfall), max(West_landfall) + binwidth, binwidth)

# Plot a histogram of landfall vs latitude
plt.figure()
plt.title('Western Number of Landfalls vs Latitude')
plt.hist(West_landfall, bins=bins)

# Put bins index for latitude
inds = np.digitize(West_landfall,bins)

# Create a list for mean vmaxs
mean_vmax =[]

bin_number = 0
while bin_number < len(bins):
	# Create list to store all vmaxs in the bin
	vmaxs = []

	latitude_number = 0

	while latitude_number < len(West_landfall):
		# Check for points in the bins
		if inds[latitude_number] == bin_number:
			# If the point is in the bin, add vmax to list vmaxs
			vmaxs.append(West_vmax[latitude_number])
		latitude_number += 1

	# If no point exist, add 0 to list mean vmax
	if len(vmaxs) == 0:
		mean_vmax.append(0)

	# If not, calculate and add the mean
	else:		
		mean_vmax.append(sum(vmaxs)/len(vmaxs))
	bin_number += 1
	progress(bin_number,len(bins))

# Plot mean vmax against latitude
plt.figure()
plt.title('Western Mean of Maximum Wind Speed vs Latitude')
plt.xlabel('Latitude / degree')
plt.ylabel('Mean of Maximum Windspeed at Landfall / knots')
plt.bar(bins,mean_vmax,width=0.1)

plt.show()
