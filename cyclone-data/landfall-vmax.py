"""
    This programme loads the cyclone track data and shapefile data for each country
    in order to find landfall position and other parameters upon landfall.
    
    The programme will output results into a sepearate folder and for each country.
    
"""

#Import libraries
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np
import os, os.path
import json
from LatLon import LatLon
import sys




# FUNCTIONS
# Progress bar for command line during runtime
def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  




# PARAMETER
# Set the resolution of the of the path needed in km
length_division = 10.
# List the countries that are being investigated
# countries = ['China','Japan','North-Korea','Philippines','South-Korea','Taiwan','Vietnam']
countries = ['Japan']
# Specify folder name to store output files
folder_name = 'landfall-vmax'
# Specify cyclone track data file to load
cyclone_track_file = 'cyclone-track-landfall-vmax'
# Specify the data structure of the cyclone track data 
structure = ['Lon','Lat','VMAX','CY','YYYYMMDDHH']

# Distance from land in km to be counsidered as landfall
distance_from_land = 200
# Define the range from land to sort the points
Range = 5



# METHOD
# Determine the index of longitude and latitude
index_longitude = structure.index('Lon')
index_latitude = structure.index('Lat')



# Define the relative path of the current working folder, which should be inside cyclone-data
REL_PATH = os.path.dirname(os.path.abspath(__file__))

# Read the cylone track data file
os.chdir(os.path.join(REL_PATH,'cyclone-track'))
with open('%s' % cyclone_track_file, 'rb') as file:
    source = file.read()
    cyclone_track = json.loads(source)

# cd folder containing all the countries shapefile
os.chdir(REL_PATH)

# Create a directory to store the output files

for country in countries:

    # cd the latlon folder
    os.chdir(os.path.join(REL_PATH,'latlon'))


    print 'Analysing %s' % country

    # Read the latlon file of the country
    with open('%s' %country, 'rb') as file:
        source = file.read()
        country_latlon_raw = json.loads(source)

    #List for landfall latitudes
    landfall = []
    
    # Determine whether the cyclone move into the big box
    map = Basemap(projection='cyl',resolution='c',llcrnrlon=100,\
            llcrnrlat=0,urcrnrlon=140,urcrnrlat=45)


    # Load country min & max longitude and latitude
    country_latlon = country_latlon_raw[0]
    min_longitude = country_latlon[0]
    max_longitude = country_latlon[1]
    min_latitude = country_latlon[2]
    max_latitude = country_latlon[3]

    # Load the coordinates of the coast line of the country
    country_points = country_latlon_raw[1]

    # Find landfall latitudes of each cyclone
    cyclone_number = 0

    print 'There are a total of %i cyclones' %len(cyclone_track)

    while cyclone_number < len(cyclone_track):
        each_cyclone_track = cyclone_track[cyclone_number]
        
        # Empty lists to store interesting points for a cyclone
        Interested_point = []

        # Track the points of the cyclones to see whether it crosses the big box
        point_number = 0

        while point_number < (len(each_cyclone_track[index_longitude])-1):
            longitude = (each_cyclone_track[index_longitude])[point_number]
            latitude = (each_cyclone_track[index_latitude])[point_number]
            
            next_longitude = (each_cyclone_track[index_longitude])[point_number+1]
            next_latitude = (each_cyclone_track[index_latitude])[point_number+1]

            # Check weather the poins are within the given range
            if longitude <= (max_longitude+Range) and next_longitude <= (max_longitude+Range):
                if longitude >= (min_longitude-Range) and next_longitude >= (min_longitude-Range):
                    if latitude <= (max_latitude+Range) and next_latitude <= (max_latitude+Range):
                        if latitude >= (min_latitude-Range) and next_latitude >= (min_latitude-Range):
                            temp = []
                            temp2 = []
                            for item in each_cyclone_track:
                                temp.append(item[point_number])
                            for item in each_cyclone_track:
                                temp2.append(item[point_number+1]) 
                            Interested_point.extend([temp,temp2])

            point_number += 1

        i = 0


        cyclone_landfall_points = []

        while i < (len(Interested_point)-1):
            initial_point = Interested_point[i]
            final_point = Interested_point[i+1]
            
            init_point = LatLon(initial_point[index_latitude],initial_point[index_longitude])
            fin_point = LatLon(final_point[index_latitude],final_point[index_longitude])
            dis_between = init_point.distance(fin_point)
           

            if init_point != fin_point:
                intermediate_points = map.gcpoints(initial_point[index_longitude],
                    initial_point[index_latitude],final_point[index_longitude],final_point[index_latitude],
                    (round(dis_between/length_division)+1))
                
                check = 0
                while check < len(intermediate_points[1]):
                    

                    cyclone_position = LatLon((intermediate_points[1])[check],
                                (intermediate_points[0])[check])

                    check2 = 0

                    while check2 < len(country_points):
                        check_point = LatLon((country_points[check2])[1],(country_points[check2])[0])
                        distance_calculated = cyclone_position.distance(check_point)
                        
                        # If the distane from the centre of the cyclone to land is smaller than the set value,
                        # add to list cyclone_landfall_points
                        if distance_calculated <= distance_from_land:
                            cyclone_landfall_points.append([(intermediate_points[0])[check],
                                (intermediate_points[1])[check],initial_point[2]])
                        
                        check2 += 1
                    check += 1
            i += 1
            progress(i,(len(Interested_point)-1))

        # Create bins of size 1 latitude
        bins = np.arange(0,50,1)

        # This states what bins the points belong to
        inds = np.digitize([item[1] for item in cyclone_landfall_points],bins)

        for item in bins:
            # Get index of the latitude
            latitude_index = list(bins).index(item)
            temp_points = []

            for item1 in inds:
                if item1 == latitude_index:
                    # If the points belong to the latitude bin, add to temp_points
                    temp_points.append(cyclone_landfall_points[list(inds).index(item1)])

            # If the list is not empty
            if len(temp_points) != 0:
                vmax = [v[2] for v in temp_points]
                vmax.sort(reverse=True)
                landfall.append([item,vmax[0]])
            
            
        print '%s Cyclone %i/%i done' %(country, (cyclone_number+1),len(cyclone_track))
        cyclone_number += 1


    # cd the latlon folder
    os.chdir(os.path.join(REL_PATH,folder_name))

    print 'Hello'

    with open('%s' % country,'wb') as dump:
        dump.write(json.dumps(landfall))

