###Assumptions

###Running the program
- use the following command to run the program with input file containing flow log data and lookup file containing port-protocol to tag map with default indexes as per specification of flow logs

 `python3 tagFlowLogs.py -i ./data/flowLogData.txt -l ./data/lookupTable.txt` 

- use the following command to run the program with input file containing flow log data and lookup file containing port-protocol to tag map with default indexes as per specification of flow logs

 `python3 tagFlowLogs.py -i ./data/flowLogData.txt -l ./data/lookupTable.txt` 

###Running tests

`python3 tagFlowLogsTest.py`

###Test Performed
 - unit test
 - manual test with missing file, empty file and large file.