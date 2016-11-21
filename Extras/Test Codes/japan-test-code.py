import os
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import json

# Get relative path
REL_PATH = os.path.dirname(os.path.abspath(__file__))

# cd the working directory
os.chdir(os.path.join(REL_PATH,'../cyclone-data/latlon'))

country = 'Japan'
position = [138.2529,36.2048]
latitude = position[1]
longitude = position[0]
Range = 20

# Extract boundaries for the country
right_bound  = longitude + Range
left_bound   = longitude - Range
top_bound    = latitude + Range
bottom_bound = latitude - Range

map = Basemap(projection='cyl',lat_ts=latitude,
    lat_0=latitude,lon_0=longitude,resolution='l', llcrnrlon=left_bound,
    llcrnrlat=bottom_bound, urcrnrlon=right_bound,urcrnrlat=top_bound)

map.drawcoastlines()
map.drawparallels(np.arange(bottom_bound,top_bound,10.))
map.drawmeridians(np.arange(left_bound,right_bound,10.))
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')

with open('Japan','r') as file:
	source = file.read()
	data = json.loads(source)


x = [item[0] for item in data[1]]
y = [item[1] for item in data[1]]


plt.plot(x,y,'ko')
plt.show()
