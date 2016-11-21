import matplotlib.pyplot as plt
import numpy as np
import os, os.path
import json
import sys

# PARAMETER
country = 'Philippines'

# METHOD
# Define the relative path of the current working folder, which should be inside cyclone-data
REL_PATH = os.path.dirname(os.path.abspath(__file__))


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

# Divide the country into east and west profiles
locations = [item for item in country_shapefile[1]]

east = []
west = []

point = 0
while point < len(locations):
	latitude = (locations[point])[1]
	longitude = (locations[point])[0]
	for item in locations:
		if item != locations[point]:
			if item[1] == latitude:
				if item[0] < longitude:
					east.append(locations[point])
				else:
					west.append(locations[point])
	point += 1

print 'Analysis done'


from mpl_toolkits.basemap import Basemap
map = Basemap(projection='cyl',llcrnrlon=116.9,llcrnrlat=3,urcrnrlon=127.2,urcrnrlat=19.5,resolution='l')
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')
map.drawcoastlines()

e_x = [item[0] for item in east]
e_y = [item[1] for item in east]
w_x = [item[0] for item in west]
w_y = [item[1] for item in west]

plt.plot(e_x,e_y,'ko')
plt.plot(w_x,w_y,'wo')
plt.show()