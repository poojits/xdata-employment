# -*- coding: utf-8 -*-
import sys
import os
import getopt
import json
from datetime import datetime

_features = []
_verbose = False
_helpMessage = '''
Usage:python EmploymentMetExtractor.py [-f JSON file path] [-v]

Options:
-f JSON file path --file=file

-v --verbose

'''

class Error(Exception):
    '''An error for problems with arguments on the command line.'''
    def __init__(self, msg):
        self.msg = msg

def verboseLog(message):
    if _verbose:
        print >>sys.stderr, message

def checkFilePath(filePath):
    return filePath is not None and os.path.isfile(filePath)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        try:
            opts, args = getopt.getopt(argv[1:], 'vf:', ['verbose', 'file='])
        except getopt.error, msg:
            raise Error(msg)

        if len(opts) == 0:
            raise Error(_helpMessage)
        _filePath = None

        for option, value in opts:
            if option in ('-f', '--file'):
                _filePath = value
            elif option in ('-v', '--verbose'):
                global _verbose
                _verbose = True

        if not checkFilePath(_filePath):
            raise Error("JSON file doesn't exist")

        inputFile = open(_filePath)
        jsonObject = json.load(inputFile)
        jobLastTime = 0
        if 'postedDate' in jsonObject and 'lastSeenDate' in jsonObject:
            end = datetime.strptime(jsonObject['lastSeenDate'], "%Y-%m-%d")
            start = datetime.strptime(jsonObject['postedDate'], "%Y-%m-%d")
            jobLastTime = int((end - start).total_seconds())
        jsonObject['jobLastTime'] = jobLastTime
        inputFile.close()

        outputFile = open(_filePath, "wb")
        jsonString = json.dumps(jsonObject, ensure_ascii=False, encoding='iso-8859-1')
        outputFile.write(jsonString.encode('utf8'))
        verboseLog('File name: ' + _filePath + ' jobLastTime: ' + str(jobLastTime))
        outputFile.close()


    except Error, err:
        print >>sys.stderr, sys.argv[0].split('/')[-1] + ': ' + str(err.msg)
        return 2

if __name__ == "__main__":
    sys.exit(main())
