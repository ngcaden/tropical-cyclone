"""
    This module plot maps of all the countries in East Pacific region.
    Additionally, this module helps to identify boxed regions for each country.
    
    Longitude and latitude of countries are inserted into list 'position' with
    format [longitude,latitude]. The name of the countries are inserted in list 
    'country'.
"""

# Import libraries
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch

# LONGITUDE AND LATITUDE DATA OF COUNTRIES
country = ['Philippines']
position = [[121.8,12.9]]

i = 0

while i < len(position):
    fig = plt.figure(i)
    
    # Extract latitude and longitude information
    latitude = (position[i])[1]
    longitude = (position[i])[0]

    # Define binding boundaries for the map
    Range = 30.
    right_bound  = longitude + Range
    left_bound   = longitude - Range
    top_bound    = latitude + Range
    bottom_bound = latitude - Range
    
    map = Basemap(projection='laea',lat_ts=latitude,\
            lat_0=latitude,lon_0=longitude,resolution=None, \
            llcrnrlon=left_bound,llcrnrlat=bottom_bound,\
            urcrnrlon=right_bound,urcrnrlat=top_bound)
    # draw parallels and meridians.
    map.drawparallels(np.arange(bottom_bound,left_bound,5.))
    map.drawmeridians(np.arange(left_bound,right_bound,5.))
    #map.drawmapboundary(fill_color='aqua')
    map.readshapefile(shapefile = \
        '/Users/nguyenquang30795/Desktop/BSc Project/country-shapefiles/Philippines/PHL_adm0', \
        name = 'Philippines')
    
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
    
    # Empty list to store area values
    Area = []
    
    shape = 0
    while shape < len(map.Philippines):
        # Calculate areas of each island
        area = PolygonArea(map.Philippines[shape])
        Area.append(area)
        shape += 1
    print Area
    
    Island = []
    # Get the index of the top 10 largest islands
    island = 0
    rank = 10
    while island < rank:
        Island.append([i[island] for i in sorted(enumerate(Area), key=lambda x:x[1])])
                
    plt.title("Map of %s" % country[i])
    plt.show()   
    i += 1

