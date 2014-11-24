import os
import sys
import multiprocessing as mp

help_message = '''
Usage: python divideData.py <data folder>'''
allFiles = []

def folder_exists(folderPath):
    return folderPath is not None and os.path.isdir(folderPath)

def makeDir(dir_path):
	if not folder_exists(dir_path):
		os.mkdir(dir_path)

def moveFiles(data_folder, bucketSize, bucket, isLast):
	dir_path = os.path.join(data_folder, 'data' + str(bucket+1))
	makeDir(dir_path)
	start = bucket * bucketSize
	end = len(allFiles) if isLast == True else bucketSize*(bucket+1)
	count = 0
	for i in range(start,end):
		file_path = os.path.join(data_folder, allFiles[i])
		os.system('mv ' + file_path + ' ' + dir_path)
		count = count + 1
	return (bucket,count)

def callback_log(callback_data):
	bucket = callback_data[0]
	files_moved = callback_data[1]
	print '%d files moved in bucket %d' % (files_moved,bucket)

def main(argv):
	argc = len(argv)
	if(argc < 2):
		print help_message
		sys.exit()
	data_folder = argv[1]
	print 'Reading directory listing'
	global allFiles
	allFiles = [ f for f in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder,f))]
	print 'Directory listing read'
	cores = mp.cpu_count()
	pool = mp.Pool(cores)
	bucketSize = len(allFiles) / cores
	for bucket in range(0,cores):
		isLast = True if bucket==cores-1 else False
		pool.apply_async(moveFiles, args =(data_folder,bucketSize,bucket,isLast), callback = callback_log)
	pool.close()
	pool.join()

if __name__ == "__main__":
	main(sys.argv)