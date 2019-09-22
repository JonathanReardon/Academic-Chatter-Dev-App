#!/usr/bin/env python

import tweepy
import time
from time import sleep
import datetime
import sys

# insert Twitter Dev App security keys and tokens
consumer_key        = "***************************"
consumer_secret     = "**************************************************"
access_token        = "**************************************************"
access_token_secret = "**************************************************"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

# set search content, we prioritize tweets that have tagged Academic Chatter directly (search 1)
search1  = ("@AcademicChatter OR #academicchatter OR #acchat -filter:retweets AND -filter:replies")

# if we don't find tweets that included our tag then we search for general academic twitter hashtags 
search2  = ("#phdchat OR #academictwitter OR #acwri OR #ecrchat OR #phdadvice OR #phdlife OR #gradschool -filter:retweets AND -filter:replies")

# add troll/abusive/exploitative accounts to this list never to share them
never_share = ["@account not to share 1", "@account not to share 2"]

running = True
while running == True:

    x = [1,2,3,4,5,6,7,8,9,10]
    random.shuffle(x)
    print("first element of x:", x[0])

    if x[0]<8:
        search_lists = [search1, search2]
        print(search_lists[0])
    elif x[0] >= 8:
        search_lists = [search2, search1]
        print(search_lists[0])

    RateLimitCounter1=0
    RateLimitCounter2=0

    # first search for tweets containing Academic Chatter tags (Search 1)
    for tweet in tweepy.Cursor(api.search,
                               q=search1,
                               result_type="recent",
                               lang='en').items(1):

         # if found tweet was shared by one of these users (spam/abuse/troll), then don't share (break loop) 
        if tweet.user.screen_name in never_share:
	    print("Avoiding spam user: ", tweet.user.screen_name)
            break

        if RateLimitCounter1==0:
            # information for output logs
	    print("username: ", tweet.user.screen_name)
            print("tweet content: ", tweet.text)
            print("length of original tweet: ", len(tweet.text))
 
            # if found tweet contains any of these strings, don't share (block inappropriate content)
	    if "#inappropriate-word1" in tweet.text or "#inappropriate-word2" in tweet.text:
	        print "spam found"
	        break

            RateLimitCounter2+=1
            try:
	        tweet.retweet()
	        RateLimitCounter1+=1

	    except tweepy.TweepError as e:
	        print(e)
	        if 'Failed to send request' in e.reason:
	           time.sleep(240)
            except StopIteration:
	        break

        if RateLimitCounter1==0:
            print("second search..")
            RateLimitCounter2+=1
            # second search for tweets containing general academic twitter hashtags (search 2)
            for tweet in tweepy.Cursor(api.search,
                                       q=search2,
                                       result_type="recent",
                                       lang='en').items(1):
                
                 # if found tweet was shared by one of these users (spam/abuse/troll), then don't share (break loop)
                 if tweet.user.screen_name in never_share:
                    print("Avoiding spam user: ", tweet.user.screen_name)
                    break

        	if RateLimitCounter1==0:
                    # useful for output logs
	   	    print ("tweet content: ", tweet.text)
                    print ("length of original tweet: ", len(tweet.text))
 
                    # if found tweet contains any of these strings, don't share (block inappropriate content)
	   	    if "#inappropriate-word1" in tweet.text or "#inappropriate-word2" in tweet.text:
	                print "spam found"
		        break
                try:
		    tweet.retweet()
		    RateLimitCounter1+=1
                    RateLimitCounter2+=1

		except tweepy.TweepError as e:
		    print(e)
		    if 'Failed to send request' in e.reason:
		        time.sleep(240)
                except StopIteration:
                    break
                    
    # 2 searches but found nothing to share
    if RateLimitCounter2==2:
        time.sleep(600)
        print("Did 2 searches but found nothing to share - sleeping for 600 seconds (10 mins)")
    # 2 searches and 1 share on the second search
    elif RateLimitCounter2==3:
        time.sleep(800)
        print("Did 2 searches but found something to share on the second search - sleeping for 800 seconds (15 mins)")
    # 1 search and 1 share
    else:
        time.sleep(800)
        print("Did 1 search and found tweet to share that tagged the account directly - sleeping for 800 seconds (15 mins)")
