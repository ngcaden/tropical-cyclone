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




# PARAMETERS
# Longitude and latitude of the country
country = 'Philippines'
position = [121.8,12.9]
# Define the boundaries in degrees from the centre for the country
Range = 20.
# Define the resolution in terms of latitude for the country
division = 0.1
# Define the total number of islands interested
number_of_islands = 11





# METHOD
# Get the relative path of the current working directory
REL_PATH = os.path.dirname(__file__)

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
for file in os.listdir(os.path.join(REL_PATH, '.')) :
    if file.endswith('.shp'):
        filename = os.path.join(REL_PATH, os.path.splitext(file)[0])

# Read the shapefile of the country
m1.readshapefile(shapefile = filename,
    name = 'country_raw_shape')

# Set up plot figure
fig = plt.figure(1)

# Set up a basemap in Lambert equal area projection for the country
map = Basemap(projection='laea',lat_ts=latitude,
        lat_0=latitude,lon_0=longitude,resolution=None, llcrnrlon=left_bound,
        llcrnrlat=bottom_bound, urcrnrlon=right_bound,urcrnrlat=top_bound)

# Draw parallels and meridians
map.drawparallels(np.arange(bottom_bound,top_bound,10.))
map.drawmeridians(np.arange(left_bound,right_bound,10.))

# Read the shapefile for the country
map.readshapefile(shapefile = filename,
    name = 'country_shape')

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

# Get the longitude and latitude for the small boxes
box_number = 0
while box_number < no_small_boxes:
    
    # Find the max and min of latitude of the small box
    max_small_lat = min_rounded_latitude + (box_number+1) * 0.1
    min_small_lat = min_rounded_latitude + (box_number) * 0.1
    
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
    small_lon_list.sort()
    
    f_lon_list=[]
    i=0
    tempa=[]
    while i<(len(small_lon_list)-1):        
        if abs(small_lon_list[i]-small_lon_list[i+1])<=0.1 and i < (len(small_lon_list)-2):
            tempa.append(small_lon_list[i])
            
        else:
            f_lon_list.append(sum(tempa)/float(len(tempa)))
            tempa=[]
        i+=1
        
    # Get the maximum and minimum longitudes for the boxes
    for item in f_lon_list:
        small_lonlat.extend([item,(max_small_lat+min_small_lat)/2.])


    for item in f_lon_list:
        small_lonlat_onmap_raw.append([item,(max_small_lat+min_small_lat)/2.])
    box_number += 1

# Change directory to cyclone-track
os.chdir(os.path.join(REL_PATH, '../../cyclone-data'))

# Write longitude and latitude data to a json file
with open('%s-latlon' % country,'wb') as dump:
    dump.write(json.dumps([big_box,small_lonlat]))


# Plot the corners of small boxes on map
small_lonlat_onmap_x = []
small_lonlat_onmap_y = []
for item in small_lonlat_onmap_raw:
    temp = map(item[0],item[1])
    small_lonlat_onmap_x.append(temp[0])
    small_lonlat_onmap_y.append(temp[1])

plt.plot(small_lonlat_onmap_x,small_lonlat_onmap_y, 'ko')
plt.title("Map of %s" % country)
plt.show() 