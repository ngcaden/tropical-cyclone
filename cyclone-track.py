#Import libraries
import os, os.path
import numpy as np

#List all the files in the folder
filelist = os.listdir('cyclone-data/bwp.2014.dat')

#Create empty list to store longitude and latitude information of all cyclones
cyclone_track = []
    

cyclone = 0
while cyclone < len([name for name in filelist]):
    #Get the file name
    filenameindex = filelist[cyclone]

    filename = 'cyclone-data/bwp.2014.dat/'+filenameindex
    
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
    
    #Create an empty list to store longitude and latitude of each cyclone
    data = []
    
    #Extract longitude and latitude
    i = 0
    while i < len(raw_data):
        #Get each line
        line = raw_data[i]
        #Get the longitude and latitude
        data.append([line[6],line[7]])
        i += 1
    
    cyclone_track.append(data)
    cyclone += 1
    
print cyclone_track