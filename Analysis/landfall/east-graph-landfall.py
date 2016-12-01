# PARAMETER
countries = ['Malaysia','Japan','Taiwan','Philippines']
binsize = 2.


# LIBRARY IMPORT
import matplotlib.pyplot as plt
import numpy as np
import os, os.path
import json
import sys


# FUNCTION
# Progress bar for command line during runtime
def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  


Combined_data = []

# DATA contains combined data from all countries
DATA = []

# Load data from all countries
for country in countries:

    # Open and loads data from every country
    with open('%s' % country, 'rb') as file:
        source = file.read()
        # Get data from each country
        data = json.loads(source)
        
        # Get location of landfall points
        if country =='Japan':
            for item in data:
                for item1 in item:
                    del item1[0]

        # Add to the combined data list
        DATA.append(data)


i = 0
while i < len(DATA[0]):
    sumup = []
    for item in DATA:
        sumup += item[i]

    Combined_data.append(sumup)
    i += 1

# Get the relative path of the file
REL_PATH = os.path.abspath('.')

# Create bins of size binsize
bins = np.arange(0,50,binsize)

# Collection of all landfall points
landfall = []
vmax = []
data_points = []
CHECK = []
rmax = []
R26 = []

# Load each cyclone data
cyclone_number = 0
while cyclone_number < len(Combined_data):
    
    # Load data of each cyclone
    cyclone_data = Combined_data[cyclone_number]

    landfall_location = [[round(item[1]*10)/10,round(item[0]*10)/10,
                (item[2])[2],(item[2])[4],(item[2])[3],
                item[3],item[4]] for item in cyclone_data]

    if len(landfall_location) != 0:
        
        # Check for year larger than 1980 and only include data after 1980
        year_string = str((landfall_location[0])[2])
        year = int(''.join([year_string[0],year_string[1],year_string[2],year_string[3]]))
        cy = (landfall_location[0])[4]
        cy_string = '%02d' % (cy,)

        # If the year is larger than 1980
        if year >= 1980:

            # This states what latitude bins the landfall points belong to
            inds = np.digitize([item[0] for item in landfall_location],bins)
            
            bin_number = 0
            while bin_number < len(bins):
                
                # Create a list to store latitude points that share a bin
                temp_points = []

                lat_point = 0
                while lat_point < len(inds):
                    if inds[lat_point] == bin_number:

                        # If the points belong to the latitude bin, add to temp_points
                        temp_points.append(landfall_location[lat_point])
                    lat_point += 1

                # If the there are points in the bin, add the bin to the landfall
                if len(temp_points) != 0:
                    
                    # Sort using date
                    temp_points.sort(key=lambda item:item[2])

                    
                    
                    # cd the folder of cyclone database
                    os.chdir(os.path.join(REL_PATH,'../../Database/CycloneData/%s') % str(year))
                    
                    # List all files in the current directory
                    list_of_files = [os.path.splitext(item) for item in os.listdir('.')]

                    # Generate file name
                    file_name = 'bwp%s%s' % (cy_string,str(year))

                    raw_data = []
                    for item in list_of_files:
                        
                        # If file name matches 
                        if item[0] == file_name:
                            # Open the file correspond with year and cyclone
                            with open(item[0]+item[1],'r') as f:
                                #Count the number of lines
                                lines= sum(1 for line in enumerate(f))

                            # Open the file correspond with year and cyclone
                            with open(item[0]+item[1],'r') as f:       
                                i = 0
                                while i < lines:    
                                    #Read each line
                                    temp = f.readline()
                                    #Split into individual strings before adding to raw_data
                                    raw_data.append(temp.split(','),)
                                    i += 1 
                    
                    for item in raw_data:
                        # if time data match
                        if int(item[2]) == int(year_string):
                            try:
                                rmax_value = int(item[19])
                                if rmax_value != 0:
                                    if int(item[11])==50:
                                        rmax.append(rmax_value)
                                        landfall.append(bins[bin_number])
                                        # Add the vmax of the first landfall point
                                        vmax.append((temp_points[0])[3])
                                        R26_values = []
                                        i = 13
                                        while i < 17:
                                            if int(item[i]) != 0:
                                                R26_values.append(int(item[i]))
                                            i+=1
                                        R26.append(sum(R26_values)/len(R26_values))
                            except:
                                pass

                    # Add the data of the landfall point
                    data_points.append(temp_points[0])

                bin_number += 1
        
    cyclone_number += 1
    progress(cyclone_number,len(data),'Eastern')

# Put bins index for latitude
inds = np.digitize(landfall,bins)

# Create a list for mean vmaxs
mean_vmax = []
std_vmax = []
bin_number = 0
while bin_number < len(bins):
    # Create list to store all vmaxs in the bin
    bin_vmaxs = []

    latitude_number = 0

    while latitude_number < len(landfall):
        
        # Check for points in the bins
        if inds[latitude_number] == bin_number:
            # If the point is in the bin, add vmax to list vmaxs
            bin_vmaxs.append(vmax[latitude_number])
        latitude_number += 1

    # If no point exist, add 0 to list mean vmax
    if len(bin_vmaxs) == 0:
        mean_vmax.append(0)
        std_vmax.append(0)
    
    # If not, calculate and add the mean
    else:       
        mean_vmax.append(float(sum(bin_vmaxs))/len(bin_vmaxs))
        std_vmax.append(np.std(bin_vmaxs))
        # print bins[bin_number], bin_vmaxs

    # # If vmax bin is larger than 100, plot histogram
    # if len(bin_vmaxs) >= 100:
    #     plt.figure()
    #     plt.title('Vmax Histogram Latitude %f' % bins[bin_number])
    #     plt.xlabel('Vmax')    
    #     plt.ylabel('Counts')
    #     vmax_bin = np.arange(min(bin_vmaxs),max(bin_vmaxs)+5,5)
    #     plt.hist(bin_vmaxs,vmax_bin)
    bin_number += 1
    progress(bin_number,len(bins),'vmax')


# Create a list for mean rmaxs
mean_rmax = [] 
std_rmax = []
bin_number = 0
while bin_number < len(bins):
    # Create list to store all rmaxs in the bin
    bin_rmaxs = []

    latitude_number = 0

    while latitude_number < len(landfall):
        
        # Check for points in the bins
        if inds[latitude_number] == bin_number:
            # If the point is in the bin, add rmax to list rmaxs
            bin_rmaxs.append(rmax[latitude_number])
        latitude_number += 1

    # If no point exist, add 0 to list mean rmax
    if len(bin_rmaxs) == 0:
        mean_rmax.append(0)
        std_rmax.append(0)
    
    # If not, calculate and add the mean
    else:       
        mean_rmax.append(float(sum(bin_rmaxs))/len(bin_rmaxs))
        std_rmax.append(np.std(bin_rmaxs))

    # # If rmax bin is larger than 100, plot histogram
    # if len(bin_rmaxs) >= 50:
    #     plt.figure()
    #     plt.title('rmax Histogram Latitude %f' % bins[bin_number])
    #     plt.xlabel('rmax')    
    #     plt.ylabel('Counts')
    #     rmax_bin = np.arange(min(bin_rmaxs),max(bin_rmaxs)+5,5)
    #     plt.hist(bin_rmaxs,rmax_bin)

    bin_number += 1
    progress(bin_number,len(bins),'rmax')

# Create a list for mean vmaxs
mean_R26 = []
std_R26 = []
bin_number = 0
while bin_number < len(bins):
    # Create list to store all R26s in the bin
    bin_R26s = []

    latitude_number = 0

    while latitude_number < len(landfall):
        
        # Check for points in the bins
        if inds[latitude_number] == bin_number:
            # If the point is in the bin, add R26 to list R26s
            bin_R26s.append(R26[latitude_number])
        latitude_number += 1

    # If no point exist, add 0 to list mean R26
    if len(bin_R26s) == 0:
        mean_R26.append(0)
        std_R26.append(0)
    
    # If not, calculate and add the mean
    else:       
        mean_R26.append(float(sum(bin_R26s))/len(bin_R26s))
        std_R26.append(np.std(bin_R26s))
        # print bins[bin_number], bin_R26s

    # # If R26 bin is larger than 100, plot histogram
    # if len(bin_R26s) >= 100:
    #     plt.figure()
    #     plt.title('R26 Histogram Latitude %f' % bins[bin_number])
    #     plt.xlabel('R26')    
    #     plt.ylabel('Counts')
    #     R26_bin = np.arange(min(bin_R26s),max(bin_R26s)+5,5)
    #     plt.hist(bin_R26s,R26_bin)
    bin_number += 1
    progress(bin_number,len(bins),'R26')

plt.figure()
plt.title('Eastern Number of Landfalls vs Latitude')
plt.xlabel('Latitude')    
plt.ylabel('Counts')
plt.hist(landfall, bins=bins)


plt.figure()
plt.title('Eastern Mean of Maximum Wind Speed vs Latitude')
plt.xlabel('Latitude / degree')
plt.ylabel('Mean of Maximum Windspeed at Landfall / knots')
plt.bar(bins,mean_vmax,yerr=std_vmax,width=binsize)

plt.figure()
plt.title('Eastern Mean of Maximum Wind Radius vs Latitude')
plt.xlabel('Latitude / degree')
plt.ylabel('Mean of Maximum Windspeed Radius at Landfall / nautical miles')
plt.bar(bins,mean_rmax,yerr=std_rmax,width=binsize)

plt.figure()
plt.title('Eastern Mean of R26 vs Latitude')
plt.xlabel('Latitude / degree')
plt.ylabel('Mean of R26 at Landfall / knots')
plt.bar(bins,mean_R26,yerr=std_R26,width=binsize)

# # Output data to quickplot file
# with open('Eastern-quickplot', 'wb') as file:
#     file.write(json.dumps([list(bins),binsize,landfall,mean_vmax,data_points,std_vmax]))


plt.show()
