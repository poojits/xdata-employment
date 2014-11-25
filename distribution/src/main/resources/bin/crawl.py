import os
import sys
import multiprocessing as mp
import time

help_message = '''Usage: python crawl.py <data folder>'''
time_data = []
def folder_exists(folderPath):
    return folderPath is not None and os.path.isdir(folderPath)

def crawl(data_folder, bucket):
	bucket_path = os.path.abspath(os.path.join(data_folder,'data'+str(bucket+1)))
	allFiles = [ f for f in os.listdir(bucket_path) if os.path.isfile(os.path.join(bucket_path,f))]
	t = 0
	for f in allFiles:
		file_path = os.path.join(bucket_path,f)
		command1 = '''python repack.py -f %s''' % file_path
		command2 = '''find %s | poster -u %s''' % (file_path,"http://localhost:8080/solr/oodt-fm/update/json?commit=true")
		t1 = time.time()
		os.system(command1)
		os.system(command2)
		t += (time.time()-t1)
	return (bucket,t)

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
	print 'Total time taken to Index = %f' % max(time_data)

if __name__ == "__main__":
	main(sys.argv)