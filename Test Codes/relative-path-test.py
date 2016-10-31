import os
import json
dir = os.path.dirname(__file__)


# with open(filename,'wb') as dump:
#     dump.write(json.dumps(1))

for file in os.listdir(os.path.join(dir, '.')) :
	if file.endswith('.shp'):
		print os.path.splitext(file)[0]
		filename = os.path.join(dir, os.path.splitext(file)[0])

		print filename