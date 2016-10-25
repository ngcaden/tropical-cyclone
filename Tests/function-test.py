from LatLon import LatLon

min_lat = 80
max_lat = 45.522785
min_lon = 127.636757
max_lon =145.817459

pos1 = LatLon(min_lat, max_lon)
pos2 = LatLon(min_lat, max_lon+1.)
pos3 = LatLon(min_lat, max_lon-1.)

pos4 = LatLon(min_lat, max_lon+20.)
pos5 = LatLon(min_lat, max_lon+20.+1.)
pos6 = LatLon(min_lat, max_lon+20.-1.)

print pos1.distance(pos2)
print pos1.distance(pos3)
print pos4.distance(pos5)
print pos4.distance(pos6)