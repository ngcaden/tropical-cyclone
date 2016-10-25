"""
    This programme loads the data from 'cyclone-track' and sort all the cylones that hit
    the country. Subsequently is will determine where the cyclones hit the country 
    based on location. Location data is obtained from 'country-latlon' file
    
"""

#Import libraries
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np
import time
import os, os.path
import json

start_time = time.time()

# cd the working directory
os.chdir('/Users/nguyenquang30795/Desktop/BSc Project/cyclone-data')

# Read the data file
with open('cyclone-track-pre-sorted', 'rb') as file:
    source = file.read()
    cyclone_track = json.loads(source)

# Read the latlon file
with open('taiwan-latlon', 'rb') as file:
    source = file.read()
    country_latlon = json.loads(source)

#List for landfall latitudes
landfall = []

# Width of the map used is set to be 1,000 km
width = 1e6

# Determine whether the cyclone move into the big box
map = Basemap(projection='cyl',resolution='c',llcrnrlon=100,\
        llcrnrlat=0,urcrnrlon=140,urcrnrlat=45)

min_longitude = country_latlon[0]
max_longitude = country_latlon[1]
min_latitude = country_latlon[2]
max_latitude = country_latlon[3]

# Empty lists to store interesting points
Interested_longitude = []
Interested_latitude = []


# Find landfall latitudes of each cyclone
cyclone_number = 0
while cyclone_number < len(cyclone_track):
    each_cyclone_track = cyclone_track[cyclone_number]

    # Track the points of the cyclones to see whether it crosses the big box
    point_number = 0
    all_longitude = each_cyclone_track[0]
    all_latitude = each_cyclone_track[1]

    while point_number < (len(all_longitude)-1):
        longitude = all_longitude[point_number]
        latitude = all_latitude[point_number]
        
        next_longitude = all_longitude[point_number+1]
        next_latitude = all_latitude[point_number+1]

        Range = 5
        if longitude <= (max_longitude+Range) and next_longitude <= (max_longitude+Range):
            if longitude >= (min_longitude-Range) and next_longitude >= (min_longitude-Range):
                if latitude <= (max_latitude+Range) and next_latitude <= (max_latitude+Range):
                    if latitude >= (min_latitude-Range) and next_latitude >= (min_latitude-Range):
                        print 'Hi'
                        Interested_longitude.extend([longitude,next_longitude])
                        Interested_latitude.extend([latitude,next_latitude])

        point_number += 1
    cyclone_number += 1
X = map(Interested_longitude,Interested_latitude)
print Interested_latitude
print Interested_longitude
print("--- %s seconds ---" % (time.time() - start_time))
map.drawcoastlines()
map.drawmapboundary(fill_color='aqua')
# fill continents, set lake color same as ocean color.
map.fillcontinents(color='coral',lake_color='aqua')
map.plot(X[0],X[1],'ko')
map.plot(country_latlon[0],country_latlon[2],'wo')
map.plot(country_latlon[1],country_latlon[2],'wo')
map.plot(country_latlon[0],country_latlon[3],'wo')
map.plot(country_latlon[1],country_latlon[3],'wo')
plt.show()

