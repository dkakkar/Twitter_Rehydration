"""Author:Devika Kakkar
Date: 03/07/17
Name: tweetRehydration.py
Version: 1.0
Function: This module is used for get full tweet JSON corresponding to Tweet ID  upto maximum of 100 Tweet IDs.
Input: The code needs the following input files:
idfilepath: path to file containing tweet ids
credentialfilepath = Path to file containing Twitter user's credentials such as Consumer Key, Consumer Secret, Oauth Token and Oauth Secret
outfilepath = Path to output text where the full Tweet JSON is written
Output: The output is a text file where each line is full Tweet JSON corresponding to the input Tweet ID
"""

# Import required python libraries

import tweepy
import csv
import json

# Declare the variables

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
lyst_credentials=[]

# This function verifies the user's Twitter Credentials

def verify_credentials(credentialfile):
        # Open the credentials file
        f = open(credentialfile,'r')
        for line in f:
            lyst_credentials.append(line.rstrip())
        # Read values for the crdentials in corresponsing variables    
        CONSUMER_KEY = (lyst_credentials[0])
        CONSUMER_SECRET = (lyst_credentials[1])
        OAUTH_TOKEN = (lyst_credentials[2])
        OAUTH_TOKEN_SECRET = (lyst_credentials[3])
        # Connect to Twitter
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        api = tweepy.API(auth)
        return api

# This function looks up for the Tweet corresponding to Tweet ID and writes it to the output file 

def write_tweets_bulk(twapi, idlist, outfilepath):
    # Open the output text file    
    outfile = open(outfilepath, 'w+')
    # Look up for the Tweets corresponding to Tweets Ids in the list
    tweets = twapi.statuses_lookup(id_=idlist)
    # For every Tweet in the Tweets list, write full tweet to outputfile file
    for tweet in tweets:
             outfile.write(str(tweet))
             outfile.write('\n')

 # This function creates a list of Tweet IDs (maximum upto 100, Twitter limits 100 Tweets per request) from the input file and invokes the write_tweets_bulk           

def get_tweets_bulk(twapi, idfilepath, outfilepath):

    # Read the input file and create a list of Tweet IDs
    tweet_ids = list()
    f = open(idfilepath,'r')
    reader = csv.reader(f)
    #Ignore the header
    next(reader)
    for row in reader:   
        tweet_id = row[0]
        # Keeping appending to the list of Tweet IDs upto a maximum of 100
        if len(tweet_ids) < 100:
                tweet_ids.append(tweet_id)
        #If Tweets ids more than 100, take first 100    
        else:
                tweet_ids = tweet_ids[0:99]
                
    # If IDs in Tweet IDs list, invoke the write_tweets_bulk to look up for the tweet and write to outputfile               
    if len(tweet_ids) > 0:
        #print(tweet_ids)
        write_tweets_bulk(twapi, tweet_ids, outfilepath)   
  
   
                        
def main():
    # User input file
    # Path to file containing Tweet IDs
    idfilepath = input("Enter path to id file ")
    # Path to file containing Twitter user's credentials such as Consumer Key, Consumer Secret, Oauth Token and Oauth Secret
    credentialfilepath = input("Enter path to Twitter credential file ")
    # Path to output text where the full Tweet JSON is written
    outfilepath = input ("Enter path to the output text file ")
    # Twitter API
    api=  verify_credentials(credentialfilepath)
    #Invole the function to rehydrate the bulk Tweet IDs
    get_tweets_bulk(api, idfilepath, outfilepath)
       
#Call main
if __name__ == '__main__':
    main()        
        
