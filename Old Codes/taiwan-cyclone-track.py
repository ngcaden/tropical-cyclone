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


# Define method to check for point in box
def check_in_box(lon,lat,min_lon,max_lon,min_lat,max_lat):
    if lon <= max_lon:
        if lon >= min_lon:
            if latitude <= max_latitude:
                if latitude >= min_latitude:
                    return True
                else:
                    return False
        else:
            return False

    else:
        return False

# Define method to check whether only one True is found in a list
def OP(l):
    true_found = False
    for v in l:
        if v and not true_found:
            true_found=True
        elif v and true_found:
             return False #"Too Many Trues"
    return true_found




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
with open('taiwan-latlon', 'rb') as file:
    source = file.read()
    country_latlon_raw = json.loads(source)

#List for landfall latitudes
landfall = []

# Width of the map used is set to be 1,000 km
width = 1e6

# Determine whether the cyclone move into the big box
map = Basemap(projection='cyl',resolution='c',llcrnrlon=100,\
        llcrnrlat=0,urcrnrlon=140,urcrnrlat=45)


# Load country min & max longitude and latitude
country_latlon = country_latlon_raw[0]
min_longitude = country_latlon[0]
max_longitude = country_latlon[1]
min_latitude = country_latlon[2]
max_latitude = country_latlon[3]

# Load the coordinates of the small boxes
small_box = country_latlon_raw[1]

# Find landfall latitudes of each cyclone
cyclone_number = 0
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
    print Interested_longitude
    print Interested_latitude
    i = 0
    while i < (len(Interested_latitude)-1):
        exit == False
        initial_point = [Interested_longitude[i],Interested_latitude[i]]
        final_point = [Interested_longitude[i+1],Interested_latitude[i+1]]
        
        # Check the distance between the points
        init_point = LatLon(initial_point[1],initial_point[0])
        fin_point = LatLon(final_point[1],final_point[0])
        dis_between = init_point.distance(fin_point)
        
        # Divide the track into sections of small divisions
        if initial_point != final_point:
            intermediate_points = map.gcpoints(initial_point[0],\
                initial_point[1],final_point[0],final_point[1], \
                (dis_between/length_division + 1))
            print intermediate_points
            check_point = 0
            while check_point < len(intermediate_points[0]):
                
                check_result = []
                c_pos = [(intermediate_points[0])[check_point],(intermediate_points[1])[check_point]]
                if check_point == 0:
                    print 'check please'
                    time.sleep(10)
                else:
                    c2_pos = [(intermediate_points[0])[check_point-1],(intermediate_points[1])[check_point-1]]
                
                    check = 0
                    while check < len(small_box):
                        check_result.append(check_in_box(c_pos[0],\
                            c_pos[1],\
                            small_box[check][4],small_box[check][5],\
                            small_box[check][6],small_box[check][7]))
                        check += 1
                    
                    if all(item == False for item in check_result):
                        check_point += 1
                        exit = False

                    elif OP(check_result) == False:
                        while OP(check_result) == False: 
                            print check_result
                            print c_pos, c2_pos
                            time.sleep(1)
                            check_before = check_result
                            check_result = []
                            further_intermediate_points = map.gcpoints(c_pos[0],\
                                c_pos[1],c2_pos[0], c2_pos[1], 3)
                            print further_intermediate_points
                            
                            check2 = 0
                            while check2 < len(small_box):
                                check_result.append(check_in_box((further_intermediate_points[0])[1],\
                                    (further_intermediate_points[1])[1],\
                                    small_box[check2][4],small_box[check2][5],\
                                    small_box[check2][6],small_box[check2][7]))
                                check2 += 1
                        
                            if all(item == False for item in check_result):
                                c2_pos = [(further_intermediate_points[0])[1],(further_intermediate_points[1])[1]]
                                print 'Move inwards'
                            else:
                                c_pos = [(further_intermediate_points[0])[1],(further_intermediate_points[1])[1]]
                                print 'Move outwards'

                        print 'Hello'

                        landfall_point = small_box[check_result.index(True)]
                        landfall.append([landfall_point[0],landfall_point[1],landfall_point[2],\
                            landfall_point[3] ])
                        check_point = len(intermediate_points)
                        exit = True

                    elif OP(check_result) == True:
                        check_point = len(intermediate_points)
                        
                        landfall_point = small_box[check_result.index(True)]
                        landfall.append([landfall_point[0],landfall_point[1],landfall_point[2],\
                            landfall_point[3]])
                        exit = True            

        else:
            i+=1

        if exit == False:
            i += 1

        if exit == True:
            i = (len(Interested_latitude)-1)
            print 'Landfall found'



    cyclone_number += 1
    print 'Cyclone Done'
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

