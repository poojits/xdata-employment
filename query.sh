#!/bin/bash  

QUERY1='http://127.0.0.1:8080/solr/oodt-fm/select?wt=json&indent=true&q=*:*&fq={!geofilt%20pt=-34.65,-58.34%20sfield=latlong%20d=7}&&group=true&group.field=jobtype'
QUERY2='http://127.0.0.1:8080/solr/oodt-fm/select?q={!boost%20b=recip(ms(lastSeenDate,postedDate),3.16e-11,1,1)}*:*&fq={!geofilt%20pt=-34.65,-58.34%20sfield=latlong%20d=7}&wt=json&indent=true'

curl $QUERY1
curl $QUERY2