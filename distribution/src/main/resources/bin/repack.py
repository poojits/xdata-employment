#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import pickle
import json
import geohash # need to sudo pip install python-geohash
import getopt

def main(argv=None):
  if argv is None:
    argv = sys.argv

  opts, args = getopt.getopt(argv[1:],'f:',['-file='])
  
  option, value = opts[0]
  filePath = value
  picklePath = '/Users/mlisa/Downloads/'

  with open(picklePath+'geo.pickle', 'rb') as f:
    geoCount = pickle.load(f)
    geoSum = sum([geoCount[v] for v in geoCount])

  with open(picklePath+'company.pickle', 'rb') as f:
    companyCount = pickle.load(f)
    companySum = sum([companyCount[v] for v in companyCount])

  try:
    with open( filePath, 'r') as f:
      try:
        j = json.load(f)
      except:
        return

      if j['lattitude'] == '' or j['longitude'] == '' or j['company'] == '':
        j['boost'] = 0.0
      else:
        gh = geohash.encode(float(j['lattitude']), float(j['longitude']))[:2]
        c = j['company']
        j['boost'] = (geoCount[gh]/geoSum + companyCount[c]/companySum)/2.0

        j['latitude'] = j['lattitude']
        del j['lattitude']
        
        j['location'] = j['location2']
        del j['location1']
        del j['location2']

        j['latlong'] = j['latitude'] + ',' + j['longitude']
        j['postedDate'] = j['postedDate'] + 'T00:00:00Z'
        j['firstSeenDate'] = j['firstSeenDate'] + 'T00:00:00Z'
        j['lastSeenDate'] = j['lastSeenDate'] + 'T00:00:00Z'

    with open( filePath, 'w') as f:
      jstr = json.dumps( j, ensure_ascii=False, encoding="iso-8859-1")
      f.write(jstr.encode('utf-8'))
  except:
    return    


if __name__ == "__main__":
  sys.exit(main())