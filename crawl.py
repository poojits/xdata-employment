import os
import sys
import multiprocessing as mp
import time

help_message = '''Usage: python crawl.py <data folder>'''
time_data = []
def folder_exists(folderPath):
    return folderPath is not None and os.path.isdir(folderPath)

def crawl(data_folder, bucket):
	bucket_path = os.path.join(data_folder,'data'+str(bucket+1))
	command = '''./crawler/bin/crawler_launcher --operation --launchAutoCrawler --filemgrUrl http://localhost:9000 --clientTransferer org.apache.oodt.cas.filemgr.datatransfer.InPlaceDataTransferFactory --productPath %s --mimeExtractorRepo ./crawler/policy/mime-extractor-map.xml --workflowMgrUrl http://localhost:9001 -ais TriggerPostIngestWorkflow''' % bucket_path
	t1 = time.time()
	os.system(command)
	return (bucket,time.time()-t1)

def callback_log(callback_data):
	bucket = callback_data[0]
	time_taken = callback_data[1]
	time_data[bucket] = time_taken

def main(argv):
	argc = len(argv)
	if(argc < 2):
		print help_message
		sys.exit()
	data_folder = argv[1]
	buckets = 32
	for i in range(0,buckets):
		folder_path = os.path.join(data_folder,'data'+str(i+1))
		if not folder_exists(folder_path):
			print 'This folder does not have data divided into 32 buckets'
			sys.exit()
	global time_data
	time_data = [0]*buckets
	cores = mp.cpu_count()
	pool = mp.Pool(cores)
	for bucket in range(0,buckets):
		pool.apply_async(crawl, args =(data_folder,bucket), callback = callback_log)
	pool.close()
	pool.join()
	print 'Total time taken to Index = %f' % sum(time_data)

if __name__ == "__main__":
	main(sys.argv)