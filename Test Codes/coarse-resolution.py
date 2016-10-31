import csv
from shapely.geometry import shape, mapping
from fiona import collection
import os 
from mpl_toolkits.basemap import Basemap


# Set up a basemap in cylindrical coordinates for the country
m1 = Basemap(projection='cyl',resolution=None)

# Read the shapefile of the country
m1.readshapefile(shapefile = \
    '/Users/nguyenquang30795/Desktop/BSc Project/country-shapefiles/Taiwan/TWN_adm0', \
    name = 'twn')

print m1.twn