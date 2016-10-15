#Import libraries
import numpy as np


filename = 'cyclone-data/bwp.2014.dat/bwp012014.dat'

#Count the number of lines
with open (filename) as f:
    lines= sum(1 for line in enumerate(f))

#Create an empty list for writing read infomation
data = []

#Open file for comprehension
file = open(filename, 'r')


i = 1

#Reading file
while i < lines:
    temp = file.readline()
    print temp
    data.append([temp],)
    i += 1
    
print data

