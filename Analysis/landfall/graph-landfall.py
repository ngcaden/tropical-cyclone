# PARAMETER
country = 'Vietnam'
binsize = 0.5


# LIBRARY IMPORT
import matplotlib.pyplot as plt
import numpy as np
import os, os.path
import json
import sys


# FUNCTION
# Progress bar for command line during runtime
def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  

with open('%s' % country, 'rb') as file:
    source = file.read()
    data = json.loads(source)


# METHOD
# Create bins of size binsize
bins = np.arange(0,50,binsize)

# Collection of all landfall points
landfall = []
vmax = []
data_points = []

# Load each cyclone data
cyclone_number = 0
while cyclone_number < len(data):
    
    # Load data of each cyclone
    cyclone_data = data[cyclone_number]

    # Get location of landfall points
    if country == ('Vietnam' or 'Taiwan' or 'Japan'):
        landfall_location = [[round(item[0]*10)/10,round(item[1]*10)/10,
                (item[3])[2],(item[3])[4],(item[3])[3],
                item[4],item[5]] for item in cyclone_data]
    else:
        landfall_location = [[round(item[1]*10)/10,round(item[0]*10)/10,
                (item[2])[2],(item[2])[4],(item[2])[3],
                item[3],item[4]] for item in cyclone_data]

    if len(landfall_location) != 0:

        # This states what bins the points belong to
        inds = np.digitize([item[0] for item in landfall_location],bins)
        
        bin_number = 0
        while bin_number < len(bins):
            # Create a list to store points that share a bin
            temp_points = []

            lat_point = 0
            while lat_point < len(inds):
                if inds[lat_point] == bin_number:
                    # If the points belong to the latitude bin, add to temp_points
                    temp_points.append(landfall_location[lat_point])
                lat_point += 1

            # If the there are points in the bin, add the bin to the landfall
            if len(temp_points) != 0:
                landfall.append(bins[bin_number])

                # Sort using date
                temp_points.sort(key=lambda item:item[2])

                # Add the vmax of the first landfall point
                vmax.append((temp_points[0])[3])

                # Add the data of the landfall point
                data_points.append(temp_points[0])

            bin_number += 1
        
    cyclone_number += 1
    progress(cyclone_number,len(data),'%s' % country)

# Put bins index for latitude
inds = np.digitize(landfall,bins)

# Create a list for mean vmaxs
mean_vmax =[]

bin_number = 0
while bin_number < len(bins):
    # Create list to store all vmaxs in the bin
    bin_vmaxs = []

    latitude_number = 0

    while latitude_number < len(landfall):
        
        # Check for points in the bins
        if inds[latitude_number] == bin_number:
            # If the point is in the bin, add vmax to list vmaxs
            bin_vmaxs.append(vmax[latitude_number])
        latitude_number += 1

    # If no point exist, add 0 to list mean vmax
    if len(bin_vmaxs) == 0:
        mean_vmax.append(0)

    # If not, calculate and add the mean
    else:       
        mean_vmax.append(sum(bin_vmaxs)/len(bin_vmaxs))
    bin_number += 1

plt.figure()
plt.title('%s Number of Landfalls vs Latitude' % country)
plt.xlabel('Latitude')    
plt.ylabel('Counts')
plt.hist(landfall, bins=bins)


plt.figure()
plt.title('%s Mean of Maximum Wind Speed vs Latitude' % country)
plt.xlabel('Latitude / degree')
plt.ylabel('Mean of Maximum Windspeed at Landfall / knots')
plt.bar(bins,mean_vmax,width=binsize)

# Output data to quickplot file
with open('%s-quickplot' % country, 'wb') as file:
    file.write(json.dumps([list(bins),binsize,landfall,mean_vmax,data_points]))


plt.show()
