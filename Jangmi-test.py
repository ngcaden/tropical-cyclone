#Import libraries
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np
import time

start_time = time.time()

# Jangmi typhoon data
lon = [129.2, 128.5, 128.0, 127.3, 126.6, 126.0, 125.3, 124.6, 123.9, 123.2, 122.8, 122.5, 122.2, 121.7, 120.8, 120.2, 119.6, 119.0, 118.6]
lat = [7.6, 7.7, 7.9, 8.2, 8.6, 8.9, 9.4, 9.8, 9.9, 9.8, 9.7, 9.5, 9.3, 8.8, 8.1, 7.6, 7.2, 6.8, 6.6]

# Get test points
lon_0, lon_1 = lon[4], lon[5]
lat_0, lat_1 = lat[4], lat[5]

# Calculate the distance between 2 points
# Rough width = 1/2 the circumference of the Earth
width = 1e7

# setup azimuthal equidistant projection basemap for calculating distance 
# between 2 points
map = Basemap(width=width,height=width,projection='aeqd',resolution=None,
            lat_0=lat_0,lon_0=lon_0)

point_0 = map(lon_0, lat_0)
point_1 = map(lon_1, lat_1)
distance = np.sqrt( (point_1[0] - point_0[0])**2 + (point_1[1] - point_0[1])**2 )


# setup azimuthal equidistant projection basemap to find landfall
map = Basemap(width=10000.,height=10000.,projection='aeqd',resolution='i',
            lat_0=lat_1,lon_0=lon_1)
#map.shiftgrid(lon0=lon_0,start=False)
          
          
#print map.lat_0
#map.lon_0 = lon_0
#locations = np.c_[x, y]
#
#polygons = [Path(p.boundary) for p in map.landpolygons]
#
#result = np.zeros(len(locations), dtype=bool) 
#
#for polygon in polygons:
#
#    result += np.array(polygon.contains_points(locations))
#
#print result
#
#map.drawcoastlines()
#map1.drawcoastlines()
## draw a boundary around the map, fill the background.
## this background will end up being the ocean color, since
## the continents will be drawn on top.
#map.drawmapboundary(fill_color='aqua')
#map1.drawmapboundary(fill_color='aqua')
## fill continents, set lake color same as ocean color.
#map.fillcontinents(color='coral',lake_color='aqua')
#map1.fillcontinents(color='coral',lake_color='aqua')
#
#plt.show()

print("--- %s seconds ---" % (time.time() - start_time))