from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# resolution = 'c' means use crude resolution coastlines.
map = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution='c',lat_1=10.,lat_2=15,lat_0=32,lon_0=128)
print map.landpolygons

map.drawcoastlines()
# draw a boundary around the map, fill the background.
# this background will end up being the ocean color, since
# the continents will be drawn on top.
map.drawmapboundary(fill_color='aqua')
# fill continents, set lake color same as ocean color.
map.fillcontinents(color='coral',lake_color='aqua')
plt.show()