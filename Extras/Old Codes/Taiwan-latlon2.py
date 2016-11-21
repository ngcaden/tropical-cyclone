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



# Change directory to cyclone-track
os.chdir('/Users/nguyenquang30795/Desktop/BSc Project/cyclone-data')

# Write longitude and latitude data to a json file
with open('taiwan-latlon2','wb') as dump:
    dump.write(json.dumps([big_box,island_latlon]))







