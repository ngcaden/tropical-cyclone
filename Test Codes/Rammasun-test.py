#Import libraries
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np
import time
from urllib2 import urlopen
import json
from geopy.distance import great_circle

# Get country method
def getplace(location):
    url = "http://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false" % (location[1], location[0])
    v = urlopen(url).read()
    j = json.loads(v)
    components = j['results'][0]['address_components']
    country = None
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
    return str(country)


# PARAMETERS
resolution = 'c'
point_distance = 5.e5

# RESULTS
landfall = []
landfall_country_raw = []
landfall_raw = []
landfall_country = []

# Rammasun typhoon DATA
lon = [152.9, 152.1, 151.4, 150.7, 150.0, 149.5, 148.8, 147.6, 146.2, 144.7, 143.4, 141.9, 140.5, 138.4, 136.2, 134.2, 132.4, 130.6, 130.6, 129.2, 129.2, 128.2, 128.2, 128.2, 127.0, 127.0, 127.0, 125.6, 125.6, 125.6, 124.6, 124.6, 124.6, 123.5, 123.5, 123.5, 122.1, 122.1, 122.1, 120.6, 120.6, 120.6, 119.1, 119.1, 119.1, 117.8, 117.8, 117.8, 116.9, 116.9, 116.9, 115.8, 115.8, 115.8, 115.0, 115.0, 115.0, 114.3, 114.3, 114.3, 113.4, 113.4, 113.4, 112.3, 112.3, 112.3, 111.3, 111.3, 111.3, 110.3, 110.3, 110.3, 109.4, 109.4, 109.4, 108.3, 108.3, 108.3, 107.4, 107.4, 107.4, 106.5, 106.5, 105.5, 104.4, 103.3]
lat = [8.5, 8.8, 9.5, 10.4, 11.3, 11.9, 12.7, 13.3, 13.6, 13.6, 13.7, 13.7, 13.7, 13.7, 13.7, 13.6, 13.7, 13.3, 13.3, 12.8, 12.8, 12.6, 12.6, 12.6, 12.7, 12.7, 12.7, 12.7, 12.7, 12.7, 13.0, 13.0, 13.0, 13.4, 13.4, 13.4, 13.8, 13.8, 13.8, 14.3, 14.3, 14.3, 14.8, 14.8, 14.8, 15.2, 15.2, 15.2, 15.6, 15.6, 15.6, 16.3, 16.3, 16.3, 16.9, 16.9, 16.9, 17.5, 17.5, 17.5, 18.4, 18.4, 18.4, 19.1, 19.1, 19.1, 19.9, 19.9, 19.9, 20.4, 20.4, 20.4, 21.0, 21.0, 21.0, 21.8, 21.8, 21.8, 22.5, 22.5, 22.5, 22.9, 22.9, 23.2, 23.5, 23.8]




point_order = 0
while point_order < 1:
    # Get test points
    lon_0, lon_1 = lon[point_order], lon[(point_order +1)]
    lat_0, lat_1 = lat[point_order], lat[(point_order +1)]


    # Width of the map used is set to be 1,000 km
    width = 1e7
    
    # Set up basemap at first point
    map = Basemap(width=width,height=width,projection='aeqd',resolution=resolution,
                    lat_0=25,lon_0=125)


    if lon_0 != lon_1 or lat_0 != lat_1:
        # Setup azimuthal equidistant projection basemap for calculating distance 
        # between 2 points
        
        #Start timing
        start_time = time.time()
        # Calculate the distance between 2 points
        point_0 = map(lon_0, lat_0)
        point_1 = map(lon_1, lat_1)
        distance = np.sqrt((point_1[0] - point_0[0])**2 + (point_1[1] - point_0[1])**2)
        print distance
        print("--- %s seconds ---" % (time.time() - start_time))
        
        start_time = time.time()
        print("--- %s seconds ---" % (time.time() - start_time))
        
#        # Set the number of points such that the interval between points is 10 km
#        number_points = int(distance / point_distance) + 1
#        
#        # Dissect the line connecting the 2 points
#        Points = map.gcpoints(lon_0,lat_0,lon_1,lat_1,number_points)
#        
#        # Check whether the points are on land
#        i = 0
#        Land = []
#        while i < number_points:
#            a = (Points[0])[i]
#            b = (Points[1])[i]
#
#            land = map.is_land(a,b)
#            Land.append(land)
#            i += 1
#        
#        print Land
#    
#        # Check for landfall points
#        i = 0
#        while i < (number_points-1):
#            a = Land[i]
#            b = Land[i+1]
#            if a != b:
#                #If moving from sea to land then include
#                if a == False:
#                    # Estimate the latitude of landfall
#                    longitude_raw = ((Points[0])[i+1]+(Points[0])[i])/2.
#                    latitude_raw = ((Points[1])[i+1]+(Points[1])[i])/2.
#                    #Convert to normal longitude and latitude
#                    landfall_point = map(longitude_raw,latitude_raw, inverse=True)
#                    landfall_raw.append(landfall_point)
#                    landfall_country_raw.append(getplace(landfall_point))
#            i += 1
# 
    
    
    point_order += 1 
#
#
#landfall_order = 0
#while landfall_order < len(landfall_country_raw):
#    x = landfall_country_raw[landfall_order]
#    if x not in landfall_country:
#        landfall_country.append(x)
#        landfall.append(landfall_raw[landfall_order])
#    landfall_order += 1
#print landfall_raw
#print landfall_country_raw
#print landfall_country
#print landfall



map.drawcoastlines()
# draw a boundary around the map, fill the background.
# this background will end up being the ocean color, since
# the continents will be drawn on top.
map.drawmapboundary(fill_color='aqua')
# fill continents, set lake color same as ocean color.
map.fillcontinents(color='coral',lake_color='aqua')
plt.show()
