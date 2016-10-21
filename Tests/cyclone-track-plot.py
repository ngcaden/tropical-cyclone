#Import libraries
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np
import time
import os, os.path
import json

# cd the working directory
os.chdir('/Users/nguyenquang30795/Desktop/BSc Project/cyclone-data')

# Read the data file
with open('cyclone-track', 'rb') as file:
    source = file.read()
    cyclone_track = json.loads(source)

m = Basemap(projection='cyl',llcrnrlat=0,urcrnrlat=60,\
            llcrnrlon=90,urcrnrlon=160,resolution='c')
m.drawcoastlines()
m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
m.drawparallels(np.arange(0.,60.,10.))
m.drawmeridians(np.arange(90.,160.,10.))
m.drawmapboundary(fill_color='aqua')
plt.title('Cyclone Track Post-sorted')
cyclone_number = 0
while cyclone_number < len(cyclone_track):
    lon = (cyclone_track[cyclone_number])[0]
    lat = (cyclone_track[cyclone_number])[1]
    plt.plot(lon,lat,'-')
    cyclone_number += 1
plt.show()