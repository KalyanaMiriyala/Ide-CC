import re
import codecs
import json
import sys
from datetime import datetime, date, time

numOfUnicodeTweets = 0 #Counter to hold tweets with unicode characters
hashTagPat = re.compile(r'(?<=\s)#\w+') #Pattern to search for hash tags in tweets
timerStart = None #Variable to hold Start time of the minute window, moves as new tweets are read
nodetup = () #Tuple used to store new hash tag and time attribute
aList = [] #Temporary list used to generate nodetup
prevMinTagNodes = [] #List that keeps all the hash tags encountered in last one minute
tagNodes = {} #Dictionary that holds all the hash tags and there degree seen in last minute

#Function to replace escape characters
def replace_espaces(s):
    r_replace = re.compile("[\n\t]")
    s = s.replace('\/', '/')
    s = s.replace('\\', '\\')
    s = s.replace('\’', '’')
    s = s.replace('\”', '”')
    s = s.replace('\s', '')
    s = s.replace('\r', '')
    s = s.replace('\f', '')
    s = s.replace('\v', '')
    s = r_replace.sub(' ',s)
    return s


with open(sys.argv[2], 'wt') as tweetsF: #Open file to write tweets and time stamp
    with open(sys.argv[3], 'wt') as degreeF: #Open file to write graph degree for last minute
        with open(sys.argv[1], 'r') as f: #Open file to read Jason file with tweets
            for line in f:
                tweet = json.loads(line)  # load it as Python dict
                if "text" not in tweet:
                    continue
                tweetLine = tweet['text']
                tweetTime = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
                if timerStart is None:
                    timerStart = tweetTime

                #Remove Unicode characters
                tweetLine2 = tweetLine.encode('ascii', 'ignore').decode('unicode_escape')

                #Increment the counter to track tweets with unicode, by comparing length of tweet before and  after unicode removal
                if (len(tweetLine) != len(tweetLine2)):
                    numOfUnicodeTweets += 1

                #map escape characters as specified in challenge
                tweetline2 = replace_espaces(tweetLine2).strip()
                if (len(tweetline2) > 0):
                    print(tweetline2 + " (timestamp: " + tweet['created_at'] + ")", file=tweetsF)

                #Extract Hashtags from the tweet
                hashTags = hashTagPat.findall(tweetline2)

                if len(hashTags) > 1: #If a tweet has > 1 hash tags use them to compute graph degree
                    for iterHash in hashTags:
                        itemTag = iterHash.upper() #convert hash tag to upper case
                        aList.append(itemTag)
                        aList.append(tweetTime)
                        nodeTuple = tuple(aList)
                        aList.clear()
                        #Add hash tag to List along with time stamp
                        prevMinTagNodes.append(nodeTuple)
                        #Update Dictionary Node element to reflect new degree, degree for each hash tag in tweet is #of tages -1
                        if itemTag not in tagNodes:
                            tagNodes[itemTag] = len(hashTags) - 1
                        else:
                            tagNodes[itemTag] += len(hashTags) - 1

                timeDiff = timerStart - tweetTime
                #Remove the tweets that have fallen off the window, adjust the Node degree and compute average
                if (timeDiff.seconds >= 60):
                    for iter in range(len(prevMinTagNodes)):
                        if (tweetTime - prevMinTagNodes[0][1]).seconds >= 60:
                            if tagNodes[prevMinTagNodes[0][0]] == 1: #Drop the Hashtag with one degree as it has fallen off the window
                                del tagNodes[prevMinTagNodes[0][0]]
                            else:
                                tagNodes[prevMinTagNodes[0][0]] -= 1 #Decrement the degree for hash tag that has fallen off
                            del prevMinTagNodes[0]
                        else:
                            timerStart = prevMinTagNodes[0][1] #Move the Start time to shift the window
                            break
                    #Compute Graph degree for the last minute
                    graphDeg = 0
                    nodeDegrees = tagNodes.values()
                    for degreeIter in nodeDegrees:
                        graphDeg += degreeIter

                    if len(tagNodes) > 0:
                        avgGraphDeg = graphDeg / len(tagNodes)
                    else:
                        avgGraphDeg = 0

                    print('%.2f' % avgGraphDeg, file=degreeF)


    print(str(numOfUnicodeTweets) + " tweets contained unicode.", file=tweetsF)
tweetsF.close()
degreeF.close()
f.close()
