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
from LatLon import LatLon
import sys


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben



# Set the resolution of the of the path needed in km
length_division = 10.

start_time = time.time()

# cd the working directory
os.chdir('/Users/nguyenquang30795/Desktop/BSc Project/cyclone-data')

# Read the data file
with open('cyclone-track-pre-sorted', 'rb') as file:
    source = file.read()
    cyclone_track = json.loads(source)

# Read the latlon file
with open('taiwan-latlon2', 'rb') as file:
    source = file.read()
    country_latlon_raw = json.loads(source)

#List for landfall latitudes
landfall = []

# Width of the map used is set to be 1,000 km
width = 1e6

# Distance from land in km
distance_from_land = 200

# Determine whether the cyclone move into the big box
map = Basemap(projection='cyl',resolution='c',llcrnrlon=100,\
        llcrnrlat=0,urcrnrlon=140,urcrnrlat=45)


# Load country min & max longitude and latitude
country_latlon = country_latlon_raw[0]
min_longitude = country_latlon[0]
max_longitude = country_latlon[1]
min_latitude = country_latlon[2]
max_latitude = country_latlon[3]

# Load the coordinates of the coast line of the country
country_points = country_latlon_raw[1]

# Find landfall latitudes of each cyclone
cyclone_number = 0

print 'There are a total of %i cyclones' %len(cyclone_track)

while cyclone_number < len(cyclone_track):
    each_cyclone_track = cyclone_track[cyclone_number]
    
    # Empty lists to store interesting points for a cyclone
    Interested_longitude = []
    Interested_latitude = []

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
                        Interested_longitude.extend([longitude,next_longitude])
                        Interested_latitude.extend([latitude,next_latitude])

        point_number += 1

    i = 0

    while i < (len(Interested_latitude)-1):
        initial_point = [Interested_longitude[i],Interested_latitude[i]]
        final_point = [Interested_longitude[i+1],Interested_latitude[i+1]]
        init_point = LatLon(initial_point[1],initial_point[0])
        fin_point = LatLon(final_point[1],final_point[0])
        dis_between = init_point.distance(fin_point)

        if initial_point != final_point:
            intermediate_points = map.gcpoints(initial_point[0],
                initial_point[1],final_point[0],final_point[1],
                (dis_between/length_division + 1))
            check = 0
            while check < len(intermediate_points):
                cyclone_position = LatLon((intermediate_points[1])[check],(intermediate_points[0])[check])
                check2 = 0
                check_result = []
                while check2 < len(country_points):
                    check_point = LatLon((country_points[check2])[1],(country_points[check2])[0])
                    distance_calculated = cyclone_position.distance(check_point)
                    if distance_calculated <= distance_from_land:
                        check_result.append([True,distance_calculated,check2])
                    else:
                        check_result.append([False,distance_calculated,check2])
                    check2 += 1
                
                if all(item[0] == False for item in check_result): 
                    check += 1

                else:
                    check_result.sort(key = lambda x:x[1])
                    chosen = country_points[((check_result[0])[2])]
                    landfall.append(chosen)
                    check = len(intermediate_points)
                    i = len(Interested_latitude)
            progress(i,(len(Interested_latitude)-1))
                
        i += 1
    print 'Cyclone %i/%i done' %((cyclone_number+1),len(cyclone_track))
    cyclone_number += 1


print landfall

print("--- %s seconds ---" % (time.time() - start_time))
# map.drawcoastlines()
# map.drawmapboundary(fill_color='aqua')
# # fill continents, set lake color same as ocean color.
# map.fillcontinents(color='coral',lake_color='aqua')
# map.plot(X[0],X[1],'ko')
# map.plot(country_latlon[0],country_latlon[2],'wo')
# map.plot(country_latlon[1],country_latlon[2],'wo')
# map.plot(country_latlon[0],country_latlon[3],'wo')
# map.plot(country_latlon[1],country_latlon[3],'wo')
# plt.show()

