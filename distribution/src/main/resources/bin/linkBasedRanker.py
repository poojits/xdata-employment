import json
import geohash # need to sudo pip install python-geohash
import sys, os
import pickle
import getopt

argv = sys.argv
opts, args = getopt.getopt(argv[1:],'d:',['-dir='])
option, value = opts[0]

geoCount = dict()
companyCount = dict()

rootPath = value.rstrip('/')+'/'
picklePath = './'

# folderList =[folder for folder in os.listdir(rootPath) if os.path.isdir(rootPath+folder)]

# for folder in folderList:
fileList = [file for file in os.listdir(rootPath) if file.lower().endswith('.json')]

for file in fileList:
	filePath = rootPath+ file
	with open( filePath, 'r') as f:
		j = json.load(f)
		if j['lattitude'] == '' or j['longitude'] == '' or j['company'] == '':
			continue
		gh = geohash.encode(float(j['lattitude']), float(j['longitude']))[:2]
		if gh in geoCount:
			geoCount[gh] = geoCount[gh] + 1
		else:
			geoCount[gh] = 1.0

		c = j['company']
		if c in companyCount:
			companyCount[c] = companyCount[c] + 1
		else:
			companyCount[c] = 1.0


print 'company', len(companyCount)
print 'sum geo', len(geoCount)

with open(picklePath + 'geo.pickle', 'wb') as f:
	pickle.dump(geoCount, f)

with open(picklePath + 'company.pickle', 'wb') as f:
	pickle.dump(companyCount, f)
