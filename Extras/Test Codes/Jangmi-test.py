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

resolution = 'l'

start_time = time.time()

# Jangmi typhoon data
lon = [129.2, 128.5, 128.0, 127.3, 126.6, 126.0, 125.3, 124.6, 123.9, 123.2, 122.8, 122.5, 122.2, 121.7, 120.8, 120.2, 119.6, 119.0, 118.6]
lat = [7.6, 7.7, 7.9, 8.2, 8.6, 8.9, 9.4, 9.8, 9.9, 9.8, 9.7, 9.5, 9.3, 8.8, 8.1, 7.6, 7.2, 6.8, 6.6]


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