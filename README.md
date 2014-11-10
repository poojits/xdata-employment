 Xdata-Employment
=============================================================

Installation
===============
1. Make sure to have JAVA 1.7 (oracle-java7 and NOT openjdk).
2. Run ```export JAVA_HOME="/usr/lib/jvm/java-7-oracle"``` in order to set this as an environment variable.
3. Make sure to have ```python-dev, maven2``` installed.
4. Make sure that ```ETLLIB``` is installed in ```/usr/local/bin``` so that it is available throughtout the system. 
5. Now, install ```python-geohash```, which is our dependency of link based re-ranking algorithm by, ```sudo apt-get install python-geohash```.
6. Build the package by running the following commands
```
mv xdata-employment xdata-employment-src/
mkdir xdata-employment
cd xdata-employment-src
mvn package -Pfm-solr-catalog
tar zxvf distribution/target/xdata-employment-distribution-0.1-bin.tar.gz -C ../xdata-employment
cd ../xdata-employment/bin
./oodt start
cd ../
```
This will start, Apache Tomcat on port ```8080```, and start up the OODT FileManager on port ```9000``` and WorkflowManager on port ```9001```.

Running the Crawler
===================
```
cd crawler/bin
screen
time ./crawler_launcher --operation --launchAutoCrawler --filemgrUrl http://localhost:9000 --clientTransferer org.apache.oodt.cas.filemgr.datatransfer.LocalDataTransferFactory --productPath /media/hdd/dedupe --mimeExtractorRepo ../policy/mime-extractor-map.xml --workflowMgrUrl http://localhost:9001 -ais TriggerPostIngestWorkflow
CTRL+A, D
```

Open the browser to ```http://127.0.0.1:8080/solr/``` and see the files that are being indexed. Also refer to ```http://127.0.0.1:8080/opsui``` for system status.
Keep in Mind
============
1. This project is sufficient in itself, THERE IS NO NEED TO MOVE ANY LIB FILES AROUND. 
2. The parameter ```-Pfm-solr-catalog``` is not supposed to be confused with OODT Radix's parameter. We have made modifications to the assembly rules which run Lucene's Filemanager catalog and not Solr's Filemanager Catalog.
3. When building the package, downloading the maven binaries can take time, so please be patient as some servers are slow.
4. This containts SOLR as well, so please turn off other running instances of SOLR.
5. This assumes that your data files are in ```/media/hdd/dedupe```. Please make the necessary change when running ```crawler_launcher```.
6. For link based ranking, we run ```python linkBasedRanker.py -d /media/hdd/dedupe``` offline. We have already included the result of this in ```xdata-employment/distribution/src/main/resources/bin``` folder as ```*.pickle``` files.