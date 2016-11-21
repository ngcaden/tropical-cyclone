"""
    This programme loads the cyclone track data and shapefile data for each country
    in order to find landfall position and other parameters upon landfall.
    
    The programme will output results into a sepearate folder and for each country.
    
"""



# PARAMETER
# Set the resolution of the of the path needed in km
length_division = 20.
# List the countries that are being investigated
# countries = ['China','Japan','Philippines','South-Korea','Taiwan','Vietnam']
countries = ['Japan']
# Specify folder name to store output files
folder_name = 'landfall'
# Specify cyclone track data file to load
cyclone_track_file = 'cyclone-track-data'
# Specify the data structure of the cyclone track data 
structure = ['Lon','Lat','YYYYMMDDHH','CY','VMAX']

# Distance from land in km to be counsidered as landfall
distance_from_land = 200.
# Define the range from land to sort the points
Range = 5.



# LIBRARY IMPORT
from mpl_toolkits.basemap import Basemap
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



# METHOD
# Determine the index of longitude and latitude
index_longitude = structure.index('Lon')
index_latitude = structure.index('Lat')
index_time = structure.index('YYYYMMDDHH')
index_CY = structure.index('CY')
index_vmax = structure.index('VMAX')

# Define the relative path of the current working folder, which should be inside cyclone-data
REL_PATH = os.path.dirname(os.path.abspath(__file__))

# Read the cylone track data file
os.chdir(os.path.join(REL_PATH,'cyclone-track'))
with open('%s' % cyclone_track_file, 'rb') as file:
    source = file.read()
    cyclone_track = json.loads(source)

map = Basemap(projection='cyl',resolution=None,llcrnrlon=0,\
            llcrnrlat=-90,urcrnrlon=180,urcrnrlat=90)


# Find landfall data points for all countries
for country in countries:

    # cd folder containing all the countries' coastline data
    os.chdir(os.path.join(REL_PATH, '../Database/Coastline'))

    print 'Analysing %s' % country

    # Read the latlon file of the country
    with open('%s' %country, 'rb') as file:
        source = file.read()
        country_latlon_raw = json.loads(source)

    #List for landfall data points
    landfall = []
    
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

        # Track the points of the cyclones to see whether they are in the big box
        point_number = 0

        while point_number < (len(each_cyclone_track[index_longitude])-1):
            longitude = (each_cyclone_track[index_longitude])[point_number]
            latitude = (each_cyclone_track[index_latitude])[point_number]
            
            next_longitude = (each_cyclone_track[index_longitude])[point_number+1]
            next_latitude = (each_cyclone_track[index_latitude])[point_number+1]

            # Check whether the points are within the given range
            if (longitude <= (max_longitude+Range) and longitude >= (min_longitude-Range) and \
                latitude <= (max_latitude+Range) and latitude >= (min_latitude-Range)) or \
                (next_longitude <= (max_longitude+Range) and next_longitude >= (min_longitude-Range)\
                and next_latitude <= (max_latitude+Range) and next_latitude >= (min_latitude-Range)):
                    temp1 = []
                    temp2 = []

                    for item in each_cyclone_track:
                        temp1.append(item[point_number])
                        temp2.append(item[point_number+1]) 
                    
                    temp = [temp1,temp2]

                    for item in temp:
                        if (item in Interested_point) == False:
                            Interested_point.append(item)

            point_number += 1

        i = 0


        cyclone_landfall_points = []

        while i < (len(Interested_point)-1):
            initial_point = Interested_point[i]
            final_point = Interested_point[i+1]
            
            init_point = LatLon(initial_point[index_latitude],initial_point[index_longitude])
            fin_point = LatLon(final_point[index_latitude],final_point[index_longitude])
            dis_between = init_point.distance(fin_point)
            print Interested_point[i]
            print Interested_point[i+1]

            if init_point != fin_point and dis_between != 0:
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
                            cyclone_landfall_points.append([(country_points[check2])[1],(country_points[check2])[0],
                                        (country_points[check2])[1],initial_point,check,len(intermediate_points[1])])
                        
                        check2 += 1
                    check += 1
            i += 1
            
            progress(i,(len(Interested_point)-1))

        landfall.append(cyclone_landfall_points)

            
        print '%s Cyclone %i/%i done' %(country, (cyclone_number+1),len(cyclone_track))
        cyclone_number += 1


    # cd the output folder
    os.chdir(os.path.join(REL_PATH,folder_name))

    with open('%s' % country,'wb') as dump:
        dump.write(json.dumps(landfall))

