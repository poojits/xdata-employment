import json
import geohash # need to sudo pip install python-geohash
import sys, os
import pickle
import getopt

argv = sys.argv
opts, args = getopt.getopt(argv[1:],'d:',['-dir='])
option, value = opts[0]

geoCount = dict()
jobCount = dict()

rootPath = value.rstrip('/')+'/'
picklePath = './'

# folderList =[folder for folder in os.listdir(rootPath) if os.path.isdir(rootPath+folder)]

# for folder in folderList:
fileList = [file for file in os.listdir(rootPath) if file.lower().endswith('.json')]
fileCount = len(fileList)
for file in fileList:
	fileCount = fileCount - 1
	if fileCount % 100000 == 0:
		print 'Jobs left ', fileCount
	filePath = rootPath+ file
	try:
		with open( filePath, 'r') as f:
			j = json.load(f)
			if j['lattitude'] == '' or j['longitude'] == '' or j['jobtype'] == '':
				continue
			gh = geohash.encode(float(j['lattitude']), float(j['longitude']))[:2]
			if gh in geoCount:
				geoCount[gh] = geoCount[gh] + 1
			else:
				geoCount[gh] = 1.0

			c = j['jobtype']
			if c in jobCount:
				jobCount[c] = jobCount[c] + 1
			else:
				jobCount[c] = 1.0
	except:
		continue


print 'jobtype count', len(jobCount)
print 'geo count', len(geoCount)

with open(picklePath + 'geo.pickle', 'wb') as f:
	pickle.dump(geoCount, f)

with open(picklePath + 'jobtype.pickle', 'wb') as f:
	pickle.dump(jobCount, f)
