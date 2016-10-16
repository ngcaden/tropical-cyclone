#Import libraries
import os, os.path
import numpy as np

#Define a function to convert latitude and longitude strings to floats
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




os.chdir('/Users/nguyenquang30795/Desktop/BSc Project/cyclone-data')
#List all the files in the folder
filelist = os.listdir('2014')

#Create empty list to store longitude and latitude information of all cyclones
cyclone_track = []
    

cyclone = 0
while cyclone < len([name for name in filelist]):
    #Get the file name
    filenameindex = filelist[cyclone]

    filename = '2014/'+filenameindex
    
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
    
    #Create empty list for longitude and latitude seperately
    lon = []
    lat = []
    
    #Extract longitude and latitude
    i = 0
    while i < len(raw_data):
        #Get each line
        line = raw_data[i]
        
        #Get the longitude and latitude and convert it to floats
        lat.append(convert(line[6]))
        lon.append(convert(line[7]))
        i += 1
    
    #Combine longitude and latitude data to one
    data = [lon,lat]
    cyclone_track.append(data)
    cyclone += 1

file = open('cyclone-track.txt','w')
file.write('[')
for item in cyclone_track:
    file.write('%s,' % item)
    file.write(']')
file.close()
