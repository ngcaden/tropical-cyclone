import os, os.path
import json
import matplotlib.pyplot as plt
import numpy as np

# cd the working directory
os.chdir('/Users/nguyenquang30795/Desktop/BSc Project/cyclone-data')

# Read the data file
with open('landfall-latitude', 'rb') as file:
    source = file.read()
    landfall_latitude = json.loads(source)
    
print landfall_latitude

bin_size = 1.
min_edge = min(landfall_latitude)
max_edge = max(landfall_latitude)
N = (max_edge-min_edge)/bin_size
Nplus1 = N + 1
bin_list = np.linspace(min_edge, max_edge, Nplus1)

plt.hist(landfall_latitude,bins=bin_list)
plt.show()