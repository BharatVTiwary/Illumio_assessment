import sys
import getopt
import csv
from collections import defaultdict
from typing import Dict,List

# FLOW LOG V2: https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html 
DEFAULT_DST_PORT_INDEX = 6
DEFAULT_PROTOCOL_INDEX = 7

PROTOCOL_LOOKUP = dict()
PROTOCOL_FILE_PATH = './data/protocol-numbers-1.csv'

def initializeProtocolLookup():
    global PROTOCOL_LOOKUP
    try:
        with open(PROTOCOL_FILE_PATH, 'r') as filePointer:
            reader = csv.DictReader(filePointer)
            for row in reader:
                PROTOCOL_LOOKUP[row['Decimal'].strip().lower()] = row['Keyword'].strip().lower()
    except FileNotFoundError:
        print("Internal Error: Missing configuration file for protocols mapping")
        sys.exit()

def getLookup(lookupFile: str):
    lookupDict = dict()
    try:
        with open(lookupFile, 'r') as filePointer:
            reader = csv.DictReader(filePointer)
            for row in reader:
                lookupDict[(row['dstport'].strip().lower(), row['protocol'].strip().lower())] = row['tag'].strip()
    except FileNotFoundError:
        print("lookup file for lookup table data cannot be found")
        sys.exit()
    return lookupDict


def matchFlogLog(inputFile: str, lookupDict: Dict, dstPortIndex:int=DEFAULT_DST_PORT_INDEX, protocolIndex:int=DEFAULT_PROTOCOL_INDEX):
    tagCountDict, portProtocolCountDict = defaultdict(int), defaultdict(int)
    try:
        with open(inputFile, 'r') as inFile:
            for lineNumber, record in enumerate(inFile, start=1):
                fields = record.strip().split(" ")
                if len(fields) < 2:
                    raise ValueError(f"Invalid log record at line {lineNumber}, record has less than two fields.")
                if len(fields) <= max(dstPortIndex, protocolIndex):
                    raise  ValueError(f"Invalid log record at line {lineNumber}, dstport/protocol index is not exceeds fields in record.")
                if fields[protocolIndex] == '-':
                    continue
                dstPort, protocol = fields[dstPortIndex], PROTOCOL_LOOKUP[fields[protocolIndex]]
                matchedTag = lookupDict.get((dstPort, protocol), 'Untagged')
                tagCountDict[matchedTag] += 1
                portProtocolCountDict[(dstPort, protocol)] += 1
    except FileNotFoundError:
        print("input file for flow log data cannot be found")
        sys.exit()
    return (tagCountDict, portProtocolCountDict)    

def writeTagCount(tagCountDict:Dict, outputDir:str = './output'):
    try:
        print("Started writing the tag count file")
        with open(f"output/{'tagCount.txt'}", 'w') as wp:
            writer = csv.writer(wp, delimiter=" ")
            writer.writerow(['Tag', 'Count'])
            for tag,count in tagCountDict.items():
                writer.writerow([tag,count])
    except FileNotFoundError:
        print("output file cannot be written")
        sys.exit()

def writePortProtocolCount(protocolDict: Dict, outputDir:str = './output'):
    try:
        with open(f"output/{'portProtocolCount.txt'}", 'w') as wp:
            writer = csv.writer(wp, delimiter=" ")
            writer.writerow(['Port', 'Protocol', 'Count'])
            for (port, protocol),value in protocolDict.items():
                writer.writerow([port, protocol,value])
    except FileNotFoundError:
        print("output file cannot be written")
        sys.exit()

def getInputFileFromCommandLine(argv):    
    inputFile = None
    lookupFile = None
    try:
        opts, args = getopt.getopt(argv, 'hi:l:', ["help", "--inputFile", "--lookupFile"])
        print(args)
    except getopt.GetoptError:
        print('Expected Usage: tagFlowLogs.py -i <inputfile> -l <lookupfile>')
        sys.exit()
    for opt, arg in opts:
        if opt in ('-h', 'help'):
            print('tagFlowLogs.py -i <inputfile> -l <lookupfile>')
            sys.exit()
        elif opt in ('-i', '--inputFile'):
            inputFile = arg
        elif opt in ('-l', '--lookupFile'):
            lookupFile = arg
        
    if inputFile == None or lookupFile == None:
            print('Expected Usage: tagFlowLogs.py -i <inputfile> -l <lookupfile>')
            sys.exit()
    return (inputFile, lookupFile)

if __name__ == '__main__':
    inputFile, lookupFile = getInputFileFromCommandLine(sys.argv[1:])
    initializeProtocolLookup()
    lookupDict = getLookup(lookupFile)
    tagCountDict, portProtocolCountDict = matchFlogLog(inputFile, lookupDict)
    print(tagCountDict)
    print(portProtocolCountDict)
    writeTagCount(tagCountDict)
    writePortProtocolCount(portProtocolCountDict)

