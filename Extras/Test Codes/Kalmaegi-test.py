#Import libraries
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np
import time
from urllib2 import urlopen
import json

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

resolution = 'c'

start_time = time.time()

# Kalmaegi typhoon data
lon = [142.4, 141.0, 139.6, 138.2, 136.1, 133.9, 132.4, 131.2, 130.4, 129.6, 128.7, 128.7, 127.7, 127.7, 126.7, 126.7, 125.8, 125.8, 124.5, 124.5, 124.5, 123.3, 123.3, 123.3, 122.3, 122.3, 122.3, 121.3, 121.3, 121.3, 119.3, 119.3, 117.9, 117.9, 115.8, 115.8, 114.0, 114.0, 114.0, 113.0, 113.0, 113.0, 111.5, 111.5, 111.5, 109.7, 109.7, 109.7, 107.8, 107.8, 107.8, 106.1, 106.1, 104.4, 102.8, 101.1]
lat = [9.9, 10.4, 11.3, 12.8, 13.7, 13.9, 13.8, 13.7, 13.5, 13.8, 14.1, 14.1, 14.6, 14.6, 15.2, 15.2, 15.9, 15.9, 16.5, 16.5, 16.5, 17.1, 17.1, 17.1, 17.6, 17.6, 17.6, 17.9, 17.9, 17.9, 18.0, 18.0, 18.0, 18.0, 18.4, 18.4, 18.9, 18.9, 18.9, 19.6, 19.6, 19.6, 20.2, 20.2, 20.2, 20.8, 20.8, 20.8, 21.2, 21.2, 21.2, 21.7, 21.7, 22.3, 23.4, 24.0]


point_order = 0

#List for landfall latitude
landfall = []
landfall_country_raw = []
landfall_raw = []
    

while point_order < (len(lon)-1):
    plt.figure(point_order)
    
    # Get test points
    lon_0, lon_1 = lon[point_order], lon[(point_order +1)]
    lat_0, lat_1 = lat[point_order], lat[(point_order +1)]
    
    
    # Width of the map used is set to be 1,000 km
    width = 1e6
    if lon_0 != lon_1 or lat_0 != lat_1:
        # Setup azimuthal equidistant projection basemap for calculating distance 
        # between 2 points
        map = Basemap(width=width,height=width,projection='aeqd',resolution=resolution,
                    lat_0=lat_0,lon_0=lon_0)
        
        # Calculate the distance between 2 points
        point_0 = map(lon_0, lat_0)
        point_1 = map(lon_1, lat_1)
        distance = np.sqrt((point_1[0] - point_0[0])**2 + (point_1[1] - point_0[1])**2)
        
        # Set the number of points such that the interval between points is 10 km
        number_points = int(distance / 1.e4) + 1
        
        # Dissect the line connecting the 2 points
        Points = map.gcpoints(lon_0,lat_0,lon_1,lat_1,number_points)
        
        # Check whether the points are on land
        i = 0
        Land = []
        while i < number_points:
            a = (Points[0])[i]
            b = (Points[1])[i]
            Land.append(map.is_land(a,b))
            i += 1
        
        print Land
        
    
        # Check for landfall points
        i = 0
        while i < (number_points-1):
            a = Land[i]
            b = Land[i+1]
            if a != b:
                #If moving from sea to land then include
                if a == False:
                    # Estimate the latitude of landfall
                    longitude_raw = ((Points[0])[i+1]+(Points[0])[i])/2.
                    latitude_raw = ((Points[1])[i+1]+(Points[1])[i])/2.
                    #Convert to normal longitude and latitude
                    landfall_point = map(longitude_raw,latitude_raw, inverse=True)
                    landfall_raw.append(landfall_point)
                    landfall_country_raw.append(getplace(landfall_point))
            i += 1
 
    #map.drawcoastlines()
    ## draw a boundary around the map, fill the background.
    ## this background will end up being the ocean color, since
    ## the continents will be drawn on top.
    #map.drawmapboundary(fill_color='aqua')
    ## fill continents, set lake color same as ocean color.
    #map.fillcontinents(color='coral',lake_color='aqua')
    #map.plot(Points[0],Points[1],'ko')
    
    point_order += 1 

landfall_country = []

landfall_order = 0
while landfall_order < len(landfall_country_raw):
    x = landfall_country_raw[landfall_order]
    if x not in landfall_country:
        landfall_country.append(x)
        landfall.append(landfall_raw[landfall_order])
    landfall_order += 1
print landfall_raw
print landfall_country_raw
print landfall_country
print landfall
#plt.show()

print("--- %s seconds ---" % (time.time() - start_time))