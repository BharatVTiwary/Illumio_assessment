#Coding Assessment
##Description: 

Write a program that can parse a file containing flow log data and maps each row to a tag based on a lookup table. The lookup table is defined as a csv file, and it has 3 columns, dstport,protocol,tag.   The dstport and protocol combination decide what tag can be applied.   

  

For e.g.  the lookup table file can be something like: 

dstport,protocol,tag  
25,tcp,sv_P1  
68,udp,sv_P2   
23,tcp,sv_P1 
31,udp,SV_P3 
443,tcp,sv_P2   

 

The program should generate an output file containing the following: 

###Count of matches for each tag, sample o/p shown below 
 
```
Tag Counts: 

Tag.             Count 

Untagged    2 

 sv_P2          2 

 SV_P3         1 

 sv_P1          2
```
###Count of matches for each port/protocol combination 
 
```
Port/Protocol Combination Counts: 

 

Port.   Protocol. Count 

23.     tcp       1 

80      tcp       1 

68      udp      1 

25      tcp       1 

31      udp      1  

443.  tcp       1
```
 
###Requirement details: 

- Input file as well as the file containing tag mappings are plain text (ascii) files  
- The flow log file size can be up to 10 MB 
- The lookup file can have up to 10000 mappings 
- The tags can map to more than one port, protocol combinations.  for e.g. sv_P1 and sv_P2 in the sample above. 
- The matches should be case insensitive 