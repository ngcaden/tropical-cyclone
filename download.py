'''

    This programme downloads cyclone track files on the system of usno.navy.mil
    using URL method.
    
'''


import urllib
import os, os.path

#Starting from year 2009
year = 2009


#Download from 1980 to 2009
while year > 1979:
    Year = str(year)
    
    #Make new folder with the year included
    os.makedirs(Year)
    
    #cd that folder
    os.chdir(Year)
    
    #Download all the cyclones of that year
    number = 01
    while number < 45:
        
        Number = str("%02d" % (number,))
        
        #Generate URL for download
        url = "http://www.usno.navy.mil/NOOC/nmfc-ph/RSS/jtwc/best_tracks/" + Year + "/" + Year +"s-bwp/bwp" + Number + Year +".txt"
        
        print url
        
        #Generate filename
        filename = Number + Year + '.txt'
        
        #Download the file
        urllib.urlretrieve (url,filename)
        number += 1    
    
    #Go up one directory
    os.chdir('..')
    year -= 1