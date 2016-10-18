#Import libraries
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np
import time
import os, os.path
import json

start_time = time.time()

# cd the working directory
os.chdir('/Users/nguyenquang30795/Desktop/BSc Project/cyclone-data')

# Read the data file
with open('cyclone-track', 'rb') as file:
    source = file.read()
    cyclone_track = json.loads(source)


#List for landfall latitudes
landfall = []

# Width of the map used is set to be 1,000 km
width = 1e6


# Find landfall latitudes of each cyclone
cyclone_number = 0
while cyclone_number < len(cyclone_track):
    
    lon , lat = (cyclone_track[cyclone_number])[0], (cyclone_track[cyclone_number])[1]  
    print lon, lat
    point_order = 0
    
    while point_order < (len(lon)-1):
        # Get test points
        lon_0, lon_1 = lon[point_order], lon[(point_order +1)]
        lat_0, lat_1 = lat[point_order], lat[(point_order +1)]
        
        if lon_0 != lon_1 or lat_0 != lat_1:
        
            # Setup azimuthal equidistant projection basemap for calculating distance 
            # between 2 points
            map = Basemap(width=width,height=width,projection='aeqd',resolution='i',
                        lat_0=lat_0,lon_0=lon_0)
            
            # Calculate the distance between 2 points
            point_0 = map(lon_0, lat_0)
            point_1 = map(lon_1, lat_1)
            distance = np.sqrt((point_1[0] - point_0[0])**2 + (point_1[1] - point_0[1])**2)
            
            # Set the number of points such that the interval between points is 10 km
            number_points = int(distance / 1.e4) + 1.
            
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
            
            # List to record landfall raw data
            landfall_raw = []
            
            # Check for landfall points
            i = 0
            while i < (number_points -2):
                a = Land[i]
                b = Land[i+1]
                if a != b:
                    #If moving from sea to land then include
                    if a == False:
                        landfall_raw.append(i)
                i += 1
            
            # Estimate the latitude of landfall
            for item in landfall_raw:
                longitude_raw = ((Points[0])[i+1]+(Points[0])[i])/2.
                latitude_raw = ((Points[1])[i+1]+(Points[1])[i])/2.
                #Convert to normal longitude and latitude
                landfall_point = map(longitude_raw,latitude_raw, inverse=True)
                latitude = landfall_point[1]
                landfall.append(latitude)
                print latitude
        
        point_order += 1    
    
    cyclone_number += 1
        
print landfall

with open('landfall-latitude','wb') as dump:
    dump.write(json.dumps(landfall))





#map.drawcoastlines()
## draw a boundary around the map, fill the background.
## this background will end up being the ocean color, since
## the continents will be drawn on top.
#map.drawmapboundary(fill_color='aqua')
## fill continents, set lake color same as ocean color.
#map.fillcontinents(color='coral',lake_color='aqua')
#map.plot(Points[0],Points[1],'ko')
#
#plt.show()

print("--- %s seconds ---" % (time.time() - start_time))