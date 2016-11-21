"""
    This programme loads best track data of historical tropical cyclones from 
    1945-2015.

    Input data were obtained from Naval Oceanographer Portal, Joint Typhoon
    Warning Center, Western North Pacific Ocean Best Track Data.

    Data structure from source was coded in parameters in PARAMETER.  In order 
    to choose the desired output parameters and their structure, edit 
    interested_parameter in PARAMETER. Data year range can be specified in year_range
    in PARAMETER in format [start,stop]

    Output consists of cyclone data-points with desired output parameters.
    Output data is dumped in JSON-formatted in current folder with name
    specified in file_name field in PARAMETER.
    
"""


# PARAMETER

# Parameters given in the record
parameters = ['BASIN','CY', 'YYYYMMDDHH','TECHNUM', 'TECH','TAU', 'Lat', 'Lon', 'VMAX','MSLP',
'TY','RAD', 'WINDCODE','RAD1', 'RAD2','RAD3', 'RAD4','RADP', 'RRP','MRD', 'GUSTS','EYE',
'SUBREGION','MAXSEAS', 'INITIALS','DIR', 'SPEED','STORMNAME', 'DEPTH','SEAS',
'SEASCODE','SEAS1', 'SEAS2','SEAS3', 'SEAS4']

# Specify the parameters to be extracted
interested_parameter = ['Lon','Lat','YYYYMMDDHH','CY','VMAX']

# Specify the file name to output the data
file_name = 'cyclone-track-data'

# Specify year range to extract data
year_range = [1945,2015]



# LIBRARY IMPORT
import os, os.path
import numpy as np
import json
import sys



# FUNCTIONS

# (OPTIONAL) Progress bar for command-line during execution
def progress(count, total, suffix=''):
    """
    Print progress bar in command-line during excution.

    Parameters
    ----------
    count : float
        Current step count
    total : float
        Total number of steps to be carried out
    suffix: string
        Name of the progress bar

    Returns
    -------
    [===========------------] 50% ...Example
        Visual representation of the progress
    """

    # Define the length of the bar
    bar_len = 60

    # Obtain the current progress in bar length
    filled_len = int(round(bar_len * count / float(total)))

    # Obtain the current progress percentage
    percents = round(100.0 * count / float(total), 1)

    # Write visual progress bar
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    # Print on command-line
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  

# Define a function to convert latitude and longitude strings to floats
def convert(a):
    """
    Convert longitude and latitude strings to float values

    Parameters
    ----------
    a : string
        String representing longitude and latitude in the dataset
    
    Returns
    -------
    float
        Longitude and latitude float value

    """

    # Break down characters in the string
    A = list(a)

    # For each character
    for i in A:

        # Remove any spacebar
        if i == ' ':
            A.remove(i)
        
        # If North then it is positive, remove letter N
        elif i == 'N':
            A.remove(i)
            
        # If South then it is negative, add negative sign, remove letter S
        elif i == 'S':
            A.remove(i)
            A.insert(0,'-')
        
        # If East then it is positive, remove letter E       
        elif i == 'E':
            A.remove(i)
    
        # If West then it is negative, add negative sign, remove letter W
        elif i == 'W':
            A.remove(i)
            A.insert(0,'-')
        
    # Join all characters together to form a float value        
    return float("".join(A))/10.



# METHOD

# Obtain the relative path of the programme
REL_PATH = REL_PATH = os.path.dirname(os.path.abspath(__file__))



#Create empty list to store extracted information
cyclone_track = []


year = year_range[0]

while year < (year_range[1]+1):

    # Move to yearly CycloneData folder which contains best-track data of cyclones
    os.chdir(os.path.join(REL_PATH,'../../Database/CycloneData/', '%s' % year))

    #List all the files in the folder
    filelist = os.listdir('.')
    cyclone = 0

    while cyclone < len(filelist):
        # Empty list to store data from each cyclone
        data = []

        #Get the file name
        filename = filelist[cyclone]

        # Exclude .DS_Store file in MacOS
        if filename != '.DS_Store':
            
            #Create an empty list for writing read infomation
            raw_data = []
            
            # Open the file
            with open(filename,'r') as f:
                #Count the number of lines
                lines= sum(1 for line in enumerate(f))

            with open(filename,'r') as f:       
                i = 0
                while i < lines:    
                    #Read each line
                    temp = f.readline()
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
        progress(cyclone,len(filelist),'%s/%s' % (year,year_range[1]))
    year += 1

# Move back to original folder
os.chdir(REL_PATH)

# Write the recorded data to a file
with open('%s' % file_name,'wb') as dump:
    dump.write(json.dumps(cyclone_track))

