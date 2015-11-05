# Ide-CC
Insight Data Engineering Challenge

The coding-challenge is implemented in Python 3.

Extract Tweet and Calculate average degree of Vertex

The solution is built using Python Modules (re, codecs, json, sys, and datetime). 
Program employs Json module to parse the input and extract tweets and time of creation. 
One program handles both the functions of extract, cleaning tweets and computing the average Vertex Degree to avoid 2 passes 
through the input. The program employs List and Dictionary structures of Python to track hash tags and their degree. 
All hash tags seen in the last minute are maintained in the list, while Dictionary holds the hashtags along with their vertex 
degree as values. As the Minute Window shifts elements are dropped from the list for the hash tags that have fallen out of the 
window and hash tags degree in dictionary are modified to reflect that. These structures enable to efficiently traverse the data 
to compute average vertex degree with list traverse time up to O(n) for the hash tags in last minute , and O(1) for dictionary 
look ups.

Run programs
Program is launched by running run.sh Shell script:
./run.sh
The results will be available in the files tweet_output/ft1.txt and tweet_output/ft2.txt.


Dependencies
•	Python3
•	JSON
