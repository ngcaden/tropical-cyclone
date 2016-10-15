#Import libraries
import numpy as np


filename = 'cyclone-data/bwp.2014.dat/bwp012014.dat'

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

#Create empty list to store longitude and latitude information
data = []

#Extract longitude and latitude
i = 0
while i < len(raw_data):
    #Get each line
    line = raw_data[i]
    #Get the longitude and latitude
    data.append([line[6],line[7]])
    i += 1

print data