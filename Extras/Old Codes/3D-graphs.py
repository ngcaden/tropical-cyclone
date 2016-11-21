#Import libraries
import matplotlib.pyplot as plt
from matplotlib.path import Path
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PolyCollection
import numpy as np
import os, os.path
import json
import sys

# FUNCTIONS

# PARAMETER
country = 'Philippines'

# METHOD
# Define the relative path of the current working folder, which should be inside cyclone-data
REL_PATH = os.path.dirname(os.path.abspath(__file__))

# Create a basemap instance
map = Basemap(llcrnrlon=116.9,llcrnrlat=3,urcrnrlon=127.2,urcrnrlat=19.5,resolution='l')
fig = plt.figure(1)
ax = Axes3D(fig)

# ax.set_axis_off()
# ax.azim = 270
# ax.dist = 7

polys = []
for polygon in map.landpolygons:
    polys.append(polygon.get_coords())


lc = PolyCollection(polys, edgecolor='black',
                    facecolor='aqua', closed=False)

ax.add_collection3d(lc)
ax.add_collection3d(map.drawcoastlines(linewidth=0.25))
ax.add_collection3d(map.drawcountries(linewidth=0.35))


# Load the landfall data for the country
os.chdir(REL_PATH)
with open('%s' % country, 'rb') as dump:
    source = dump.read()
    data = json.loads(source)

# Load the country shapefile data
os.chdir(os.path.join(REL_PATH,'../latlon'))
with open('%s' % country, 'rb') as dump:
    source = dump.read()
    country_shapefile = json.loads(source)

min_lon = (country_shapefile[0])[0]
max_lon = (country_shapefile[0])[1]
min_lat = (country_shapefile[0])[2]
max_lat = (country_shapefile[0])[3]

lons = np.arange(min_lon,max_lon,1)
lats = np.arange(min_lat,max_lat,1)


# Create a list of small boxes
small_boxes = []

# Find out the boxes that describe the coast line of the country
lon_number = 0
while lon_number < (len(lons)-1):
	min_small_lon = lons[lon_number]
	max_small_lon = lons[lon_number+1]
	lat_number = 0 
	while lat_number < (len(lats)-1):
		min_small_lat = lats[lat_number]
		max_small_lat = lats[lat_number+1]
		for item in country_shapefile[1]:
			if item[0] <= max_small_lon and item[0] >= min_small_lon and \
			item[1] <= max_small_lat and item[1] >= min_small_lat:
				temp_small_box = [min_small_lon,max_small_lon,min_small_lat,max_small_lat]
				if temp_small_box not in small_boxes:
					small_boxes.append(temp_small_box)
		lat_number += 1
	lon_number += 1

# Create empty data stores for landfall location
location_of_landfall = []
landfall_location = []

for item in data:
	latitude = (item[0])[1]
	longitude = (item[0])[0]
	
	small_box_number = 0
	while small_box_number < len(small_boxes):
		if longitude <= (small_boxes[small_box_number])[1] and longitude >= (small_boxes[small_box_number])[0] and \
			latitude <= (small_boxes[small_box_number])[3] and latitude >= (small_boxes[small_box_number])[2]:
			landfall_location.append(small_box_number)
		small_box_number += 1

x = []
y = []
landfall_count = []	

for item in small_boxes:
	x.append((item[0]+item[1])/2.)
	y.append((item[2]+item[3])/2.)
	landfall_count.append(landfall_location.count(small_boxes.index(item)))	

x = np.array(x)
y = np.array(y)

x, y = map(x,y)

ax.bar3d(x, y, np.zeros(len(x)), 1, 1, landfall_count, color= 'r', alpha=0.8)

plt.show()
