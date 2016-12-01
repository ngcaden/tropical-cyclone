# LIBRARY IMPORT
import xarray as xr
# import matplotlib.pyplot as plt
# import numpy as np

# Unpack the dataset
ds = xr.open_dataset('HadISST_sst.nc')

SST = ds.sst

print 
