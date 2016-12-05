# LIBRARY IMPORT
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# Unpack the dataset
ds = xr.open_dataset('../Database/SeaSurfaceTemperature/HadISST_sst.nc')

# Choose the sea surface temperature variable
SST = ds.sst

# Choose time period of 1980 to 2015
SST = SST.sel(time=slice('1980-01','2015-12'))

# Create a list of the interested latitudes
lats = np.linspace(0.5,50.5,51)

# Seclect SST only for those latitudes
SST = SST.sel(latitude=lats)

# Create a list of the interested longitudes
lons = np.linspace(100.5,150.5,51)

# Seclect SST only for those longitudes
SST = SST.sel(longitude=lons)

# Group by latitude and take the mean
SST_latitude = SST.groupby('latitude').mean()

# Plot the SST and Coriolis frequency on the same axis
omega = 7.2921e-5
plt.figure()
plt.title('Plot of Sea Surface Temperature Variation vs Latitude')
plt.xlabel('Latitude / degree')
plt.ylabel('Sea Surface Temperature / degree Celcius')
plt.subplot(111)
plt.plot(lats,SST_latitude)
# plt.subplot(111)
# plt.plot(lats,30*np.sin(np.deg2rad(lats)))
plt.show()




