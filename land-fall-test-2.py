from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np
# setup lambert conformal basemap.
# lat_1 is first standard parallel.
# lat_2 is second standard parallel
# lon_0,lat_0 is central point.
map = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution='c',lat_1=10.,lat_2=15,lat_0=32,lon_0=128)
#example of cyclone positions
lons = [50., 80., 40., 31.]
lats = [70., 41., 29., 15.]

x, y = map(lons, lats)

locations = np.c_[x, y]

polygons = [Path(p.boundary) for p in map.landpolygons]

result = np.zeros(len(locations), dtype=bool) 

for polygon in polygons:

    result += np.array(polygon.contains_points(locations))

print result

map.drawcoastlines()
# draw a boundary around the map, fill the background.
# this background will end up being the ocean color, since
# the continents will be drawn on top.
map.drawmapboundary(fill_color='aqua')
# fill continents, set lake color same as ocean color.
map.fillcontinents(color='coral',lake_color='aqua')
plt.show()
