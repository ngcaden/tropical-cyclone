from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt


# Azimuthal Equidistant Projection
width = 8000000; lon_0 = 125; lat_0 = 25
plt.figure(1)
m = Basemap(width=width,height=width,projection='aeqd',resolution='c',
            lat_0=lat_0,lon_0=lon_0)
# fill background.
m.drawmapboundary(fill_color='aqua')
# draw coasts and fill continents.
m.drawcoastlines(linewidth=0.5)
m.fillcontinents(color='coral',lake_color='aqua')
# 20 degree graticule.
m.drawparallels(np.arange(-80,81,20))
m.drawmeridians(np.arange(-180,180,20))
# draw a black dot at the center.
xpt, ypt = m(lon_0, lat_0)

m.plot([xpt],[ypt],'ko')
# draw the items
plt.title('Azimuthal Equidistant Projection')




# Equidistant Cylindrical Projection
# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# resolution = 'c' means use crude resolution coastlines.
plt.figure(2)
m1 = Basemap(projection='cyl',llcrnrlat=0,urcrnrlat=60,\
            llcrnrlon=90,urcrnrlon=160,resolution='c')
m1.drawcoastlines()
m1.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
m1.drawparallels(np.arange(0.,60.,10.))
m1.drawmeridians(np.arange(90.,160.,10.))
m1.drawmapboundary(fill_color='aqua')
plt.title("Equidistant Cylindrical Projection")

plt.show()
