# PARAMETER
country = 'Western'


# LIBRARY IMPORT
import matplotlib.pyplot as plt
import numpy as np
import os, os.path
import json
import sys


# METHOD
with open('%s-quickplot' % country,'rb') as file:
	source = file.read()
	data = json.loads(source)

plt.figure()



plt.title('%s Number of Landfalls vs Latitude' % country)
plt.xlabel('Latitude')    
plt.ylabel('Counts')
plt.hist(data[2], bins=data[0])




plt.figure()
plt.title('%s Mean of Maximum Wind Speed vs Latitude' % country)
plt.xlabel('Latitude / degree')
plt.ylabel('Mean of Maximum Windspeed at Landfall / knots')
plt.bar(data[0],data[3],yerr=data[5],width=data[1])


plt.show()
