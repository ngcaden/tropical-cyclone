"""
    This programme loads the data obtained from Naval Oceanographer Portal of
    historical cyclones in the East Asia region. 

    The programme will subsequently dumps the data in JSON-formatted in folder cyclone-data
    with name specified by user.
    
"""

#Import libraries
import os, os.path
import numpy as np
import json
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

# Define a function to convert latitude and longitude strings to floats
def convert(a):
    A = list(a)
    for i in A:
        #Remove any spacebar
        if i == ' ':
            A.remove(i)
        
        #If north then it is positive, no sign
        elif i == 'N':
            A.remove(i)
            
        #If south then it is negative, add - sign
        elif i == 'S':
            A.remove(i)
            A.insert(0,'-')
        
        #If north then it is positive, no sign        
        elif i == 'E':
            A.remove(i)
    
        #If west then it is negative, add - sign
        elif i == 'W':
            A.remove(i)
            A.insert(0,'-')
        
    return float("".join(A))/10.






# PARAMETER
# Parameters given in the record
parameters = ['BASIN','CY', 'YYYYMMDDHH','TECHNUM', 'TECH','TAU', 'Lat', 'Lon', 'VMAX','MSLP',
'TY','RAD', 'WINDCODE','RAD1', 'RAD2','RAD3', 'RAD4','RADP', 'RRP','MRD', 'GUSTS','EYE',
'SUBREGION','MAXSEAS', 'INITIALS','DIR', 'SPEED','STORMNAME', 'DEPTH','SEAS',
'SEASCODE','SEAS1', 'SEAS2','SEAS3', 'SEAS4']
# Specify the parameters to be extracted
interested_parameter = ['Lon','Lat','VMAX','CY','YYYYMMDDHH']
# Specify the file name to output the data
file_name = 'cyclone-track-landfall-vmax'






# METHOD
# Define the relative path of the programme
REL_PATH = REL_PATH = os.path.dirname(os.path.abspath(__file__))

# cd the cyclone-data folder
os.chdir(os.path.join(REL_PATH,'cyclone-data'))


#Create empty list to store extracted information
cyclone_track = []


year = 1980

while year < 2015:
    print year
    #List all the files in the folder
    filelist = os.listdir(str(year))
    cyclone = 0

    while cyclone < len(filelist):
        # Empty list to store data from each cyclone
        data = []

        #Get the file name
        filenameindex = filelist[cyclone]

        filename = str(year)+'/'+filenameindex

        # Exclude .DS_Store file in MacOS
        if filenameindex != '.DS_Store':
        
            #Count the number of lines
            with open (filename) as f:
                lines= sum(1 for line in enumerate(f))
            
            #Create an empty list for writing read infomation
            raw_data = []
            
            #Open file for comprehension
            file = open(filename, 'r')
            
            #Reading file
            i = 0
            while i < lines:
                #Read each line
                temp = file.readline()
                
                #Split into individual strings before adding to raw_data
                raw_data.append(temp.split(','),)
                i += 1
            

            for item in interested_parameter:
                temp_data = []
                
                # Find the index of the parameter in a line of data
                order = parameters.index(item)
                
                i = 0
                while i < len(raw_data):
                    #Get each line
                    line = raw_data[i]
                    
                    # If the data is longitude and latitude, convert it to floats
                    if item == 'Lat' or item == 'Lon':
                        temp_data.append(convert(line[order]))
                    
                    else:
                        try:
                            temp_data.append(int(line[order]))
                        except:
                            temp_data.append(None)

                    i += 1

                # Combine the data into 1 for each cyclone
                data.append(temp_data)
         
            cyclone_track.append(data)
        
        cyclone += 1
        progress(cyclone,len(filelist))
    year += 1

with open('%s' % file_name,'wb') as dump:
    dump.write(json.dumps(cyclone_track))

