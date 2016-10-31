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


# LONGITUDE AND LATITUDE DATA OF COUNTRIES
country = 'Taiwan'
position = [120.9605,23.6978]


# Extract latitude and longitude informationof the country
latitude = position[1]
longitude = position[0]

# Define binding boundaries for the map
Range = 20.

right_bound  = longitude + Range
left_bound   = longitude - Range
top_bound    = latitude + Range
bottom_bound = latitude - Range

m1 = Basemap(projection='cyl',resolution=None)
m1.readshapefile(shapefile = \
    '/Users/nguyenquang30795/Desktop/BSc Project/country-shapefiles/Taiwan/TWN_adm0', \
    name = 'twn')

# Set up plot figure
fig = plt.figure(1)

# Set up a basemap at the centre of the country
map = Basemap(projection='laea',lat_ts=latitude,\
        lat_0=latitude,lon_0=longitude,resolution=None, llcrnrlon=left_bound,llcrnrlat=bottom_bound, urcrnrlon=right_bound,urcrnrlat=top_bound)

# Draw parallels and meridians.
map.drawparallels(np.arange(bottom_bound,top_bound,10.))
map.drawmeridians(np.arange(left_bound,right_bound,10.))

# Read shapefile
map.readshapefile(shapefile = \
    '/Users/nguyenquang30795/Desktop/BSc Project/country-shapefiles/Taiwan/TWN_adm0', \
    name = 'Taiwan')

# Empty list to store area values
Area = []

# Get areas of the islands
shape = 0
while shape < len(map.Taiwan):
    # Calculate areas of each island
    area = PolygonArea(map.Taiwan[shape])
    Area.append([area,m1.twn[shape],map.Taiwan[shape]])
    shape += 1

# Sort area values in descending order
Area.sort(key=lambda x: x[0], reverse=True)

# Empty list to store plot coordinates for the islands on map
island_on_map = []

# Empty list to store the latitude and longitude of the islands
island_latlon = []

# Get the mainland of the country
island = 1
island_order = 0 
while island_order < island:
    island_on_map.append( Polygon( np.array((Area[island_order])[2]), True ))
    # Raw location data
    temp = (Area[island_order])[1]
    island_latlon_temp = [item for item in temp]
    island_latlon.extend(island_latlon_temp)
    island_order += 1


# Shade the area of covered by the mainland    
ax      = fig.add_subplot(111)
ax.add_collection(PatchCollection(island_on_map, facecolor= 'm', edgecolor='k', linewidths=1., zorder=2))


all_latitude = [item[1] for item in island_latlon]
all_longitude = [item[0] for item in island_latlon]


# Sort the lists of longitudes and latitudes
all_longitude.sort()
all_latitude.sort()

max_latitude = all_latitude[-1]
min_latitude = all_latitude[0]

max_longitude = all_longitude[-1]
min_longitude = all_longitude[0]

big_box = [min_longitude,max_longitude,min_latitude,max_latitude]


# Define how small the small boxes are
division = 0.2

# Define the distance from land is considered landfall in km
distance_from_land = 200.


# Round latitude
max_rounded_latitude = round(max_latitude*5)/5
min_rounded_latitude = round(min_latitude*5)/5

# Find the number of small boxes
no_small_boxes = int((max_rounded_latitude - min_rounded_latitude) / 0.2)


small_lonlat =[]
small_lonlat_onmap_raw = []
box_number = 0
while box_number < no_small_boxes:
    
    # Find the max and min of latitude of the small box
    max_small_lat = min_rounded_latitude + (box_number+1) * 0.2
    min_small_lat = min_rounded_latitude + (box_number) * 0.2
    
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

    
    # Find out the distance_from_land in terms of longitude and latitude
    # Initialise points that are 1 degree apart
    test_pos = LatLon(max_small_lat,small_lon_list[0])
    test_pos_lat = LatLon((max_small_lat + 1),small_lon_list[0])
    test_pos_lon = LatLon(max_small_lat,(small_lon_list[0]+1))

    # Compute distance in degree for the distance_from_land
    distance_in_lon = distance_from_land / test_pos.distance(test_pos_lon)
    distance_in_lat = distance_from_land / test_pos.distance(test_pos_lat)

    max_ex_small_lon = small_lon_list[-1] + distance_in_lon
    min_ex_small_lon = small_lon_list[0] - distance_in_lon
    max_ex_small_lat = max_small_lat + distance_in_lat
    min_ex_small_lat = min_small_lat - distance_in_lat

    small_lonlat.append([small_lon_list[0],small_lon_list[-1],min_small_lat,max_small_lat,\
        min_ex_small_lon,max_ex_small_lon,min_ex_small_lat,max_ex_small_lat])

    small_lonlat_onmap_raw.append([small_lon_list[0],max_small_lat])
    small_lonlat_onmap_raw.append([small_lon_list[-1],max_small_lat])
    small_lonlat_onmap_raw.append([small_lon_list[0],min_small_lat])
    small_lonlat_onmap_raw.append([small_lon_list[-1],min_small_lat])
    box_number += 1

# Change directory to cyclone-track
os.chdir('/Users/nguyenquang30795/Desktop/BSc Project/cyclone-data')

# Write longitude and latitude data to a json file
with open('taiwan-latlon','wb') as dump:
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






