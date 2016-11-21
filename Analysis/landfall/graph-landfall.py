# PARAMETER
country = 'Vietnam'
binsize = 1


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

# Load each cyclone data
cyclone_number = 0
while cyclone_number < len(data):
    
    # Load data of each cyclone
    cyclone_data = data[cyclone_number]

    # Get location of landfall points
    landfall_location = [[round(item[0]*10)/10,round(item[1]*10)/10,(item[2])[2]] for item in cyclone_data]

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

            # If the list is not empty
            if len(temp_points) != 0:
                landfall.append(bins[bin_number])
                
            bin_number += 1
        
    cyclone_number += 1
    progress(cyclone_number,len(data),'%s' % country)

plt.figure()
plt.title('%s Number of Landfalls vs Latitude' % country)
plt.xlabel('Latitude')    
plt.ylabel('Counts')
plt.hist(landfall, bins=bins)
plt.show()



