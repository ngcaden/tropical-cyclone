"""
    This module plot maps the countries in East Pacific region.
    Additionally, this module helps to identify maximum and minimum longitude and latitude
    of each country.
    
    Longitude and latitude of the country are imput as 'position' with
    format [longitude,latitude]. The name of the countries are input as
    'country'.
"""

# Import libraries
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import os
import json
from LatLon import LatLon
import sys


# FUNCTIONS
# Calculation of area using shoelace method
def PolygonArea(corners):
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area

# Progress bar
def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben



# PARAMETERS
# Longitude and latitude of the country and the total number of islands interested
# countries = ['Malaysia','China','Japan','North-Korea','Philippines','South-Korea','Taiwan','Vietnam']
# positions = [[104.1954,35.8617],[138.2529,36.2048],[127.5101,40.3399],
#             [121.8,12.9],[127.7669,35.9078],[120.9605,23.6978],[108.2772,14.0583]]

countries = ['Malaysia']
positions = [[101.97,4.21]]

# numbers_of_islands = [2,2,5,1,1,11,2,1,1]
numbers_of_islands = [1]
# Define the resolution in terms of latitude for the country
division = 0.1

# Define the latitudes of the endings of coastline
# coast_bound = [[[108.03,21.55],[121.84,41.03]],[[124.36,40],[130.7,42.3]],[[126.22,37.72],[128.36,38.62]],[[104.45,10.42],[108.03,21.55]]]

coast_bound = [[[111.337,1.274],[117.59,4.17]]]


# METHOD
# Get the relative path of the current working directory
REL_PATH = os.path.dirname(os.path.abspath(__file__))

country_number = 0
while country_number < len(countries):

    # Extract the name, longitude, latitude and number of islands for the each country
    country = countries[country_number]
    print country
    position = positions[country_number]
    number_of_islands = numbers_of_islands[country_number]

    if country == 'China':
        Range = 40.
        landfind = 5.
    else:
        Range = 20.
        # landfind = 0.2
        landfind = 5.

    # Extract latitude and longitude informationof the country
    latitude = position[1]
    longitude = position[0]

    # Extract boundaries for the country
    right_bound  = longitude + Range
    left_bound   = longitude - Range
    top_bound    = latitude + Range
    bottom_bound = latitude - Range

    # Set up a basemap in cylindrical coordinates for the country
    m1 = Basemap(projection='cyl',resolution=None)

    # Find the .shp file
    for file in os.listdir(os.path.join(REL_PATH, country, '.')) :
        if file.endswith('.shp'):
            filename = os.path.join(REL_PATH, country, os.path.splitext(file)[0])

    # Read the shapefile of the country
    m1.readshapefile(shapefile = filename,
        name = 'country_raw_shape')

    # Set up plot figure
    fig = plt.figure((country_number+1))

    # Set up a basemap in Lambert equal area projection for the country
    map = Basemap(projection='laea',lat_ts=latitude,
            lat_0=latitude,lon_0=longitude,resolution=None, llcrnrlon=left_bound,
            llcrnrlat=bottom_bound, urcrnrlon=right_bound,urcrnrlat=top_bound)

    # Read the shapefile for the country
    map.readshapefile(shapefile = filename,
        name = 'country_shape')

    print 'Map loading done'

    # Empty list to store area values
    Area = []

    # Get areas of the islands
    shape = 0
    while shape < len(map.country_shape):
        # Calculate areas of each island
        area = PolygonArea(map.country_shape[shape])
        Area.append([area,m1.country_raw_shape[shape],map.country_shape[shape]])
        shape += 1

    # Sort area values in descending order
    Area.sort(key=lambda x: x[0], reverse=True)

    # Empty list to store plot coordinates for the islands on map
    island_on_map = []

    # Empty list to store the latitude and longitude of the islands
    island_latlon = []

    # Get the mainland of the country
    island = number_of_islands
    island_order = 0 
    while island_order < island:
        island_on_map.append(Polygon( np.array((Area[island_order])[2]), True ))
        # Raw location data
        temp = (Area[island_order])[1]
        island_latlon_temp = [item for item in temp]
        island_latlon.extend(island_latlon_temp)
        island_order += 1
    # Shade the area of covered by the mainland    
    ax = fig.add_subplot(111)
    ax.add_collection(PatchCollection(island_on_map, facecolor= 'm', edgecolor='k', linewidths=1., zorder=2))

    # Sort the lists of longitudes and latitudes
    all_latitude = [item[1] for item in island_latlon]
    all_longitude = [item[0] for item in island_latlon]
    all_longitude.sort()
    all_latitude.sort()
    # Extract the maximum and minimum longitude and latitude for the country
    max_latitude = all_latitude[-1]
    min_latitude = all_latitude[0]
    max_longitude = all_longitude[-1]
    min_longitude = all_longitude[0]

    # Append the maximum and minimum latidtude and longitude inside a list
    big_box = [min_longitude,max_longitude,min_latitude,max_latitude]

    # Round the bounding latitudes to the nearest divsion
    max_rounded_latitude = round(max_latitude*10)/10
    min_rounded_latitude = round(min_latitude*10)/10

    # Find the number of small boxes of latitude
    no_small_boxes = int((max_rounded_latitude - min_rounded_latitude) / 0.1)

    # Empty list to store the longitude and latitude returned
    small_lonlat =[]
    small_lonlat_onmap_raw = []


    coast_lower = coast_bound[country_number][0]
    coast_upper = coast_bound[country_number][1]

    # Get the longitude and latitude for the small boxes
    box_number = 0

    while box_number < no_small_boxes:
        
        # Find the max and min of latitude of the small box
        max_small_lat = min_rounded_latitude + (box_number+1) * 0.1
        min_small_lat = min_rounded_latitude + (box_number) * 0.1
        
        if min_small_lat >= coast_lower[1]:
        # if min_small_lat <= coast_upper[1]:
            # Create an empty list to store all the longitude within the small box
            small_lon_list = []

            small_point_number = 0
            while small_point_number < len(island_latlon):
                # Determine the longitude and latitude of the point
                small_lon = (island_latlon[small_point_number])[0]
                small_lat = (island_latlon[small_point_number])[1]

                # If the latitude lies between the range of latitude of the small box, add the longitude
                if small_lat < max_small_lat and small_lat >= min_small_lat:
                    small_lon_list.append(small_lon)
                small_point_number += 1

            # Sort the longitude within the small box
            # small_lon_list.sort(reverse=True)
            small_lon_list.sort()
            f_lon_list=[]

            i=0
            tempa=[]
            while i<(len(small_lon_list)-1):
                if abs(small_lon_list[i]-small_lon_list[i+1])<=0.1 and i < (len(small_lon_list)-2):
                    tempa.append(small_lon_list[i])
                    
                else:
                    tempa.append(small_lon_list[i])
                    f_lon_list.append(sum(tempa)/float(len(tempa)))
                    tempa=[]

                    # if min_small_lat >= coast_lower[1] and abs(small_lon_list[i]-small_lon_list[i+1])>landfind:
                    if min_small_lat >= coast_upper[1] and abs(small_lon_list[i]-small_lon_list[i+1])>landfind:
                        i = len(small_lon_list)
                    # elif small_lon_list[i+1]<coast_lower[0]:
                    elif small_lon_list[i+1]<coast_upper[0] and min_small_lat <= coast_upper[1] and abs(small_lon_list[i]-small_lon_list[i+1])>3:

                        i = len(small_lon_list)
                i+=1
                
            # Get the maximum and minimum longitudes for the boxes
            for item in f_lon_list:
                small_lonlat.append([item,(max_small_lat+min_small_lat)/2.])


            for item in f_lon_list:
                small_lonlat_onmap_raw.append([item,(max_small_lat+min_small_lat)/2.])
            
        box_number += 1
        progress(box_number, no_small_boxes)
        
    # Change directory to cyclone-track
    os.chdir(os.path.join(REL_PATH, '../cyclone-data/latlon'))

    # Write longitude and latitude data to a json file
    with open('%s' % country,'wb') as dump:
        dump.write(json.dumps([big_box,small_lonlat]))


    # Plot the corners of small boxes on map
    small_lonlat_onmap_x = []
    small_lonlat_onmap_y = []
    for item in small_lonlat_onmap_raw:
        temp = map(item[0],item[1])
        small_lonlat_onmap_x.append(temp[0])
        small_lonlat_onmap_y.append(temp[1])

    ax.plot(small_lonlat_onmap_x,small_lonlat_onmap_y, 'ko')
    ax.set_title("Map of %s" % country)
    
    country_number += 1

    os.chdir(REL_PATH)

plt.show()