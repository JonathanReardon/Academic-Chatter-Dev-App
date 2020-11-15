#!/usr/bin/env python3

import tweepy
import time
from time import sleep
import datetime
import sys
import random

from keys import keys
from ignore import accounts_to_skip

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth,wait_on_rate_limit=True)

# set search content, we prioritize tweets that have tagged Academic Chatter directly (search 1)
search1  = ("@AcademicChatter OR #academicchatter OR #acchat -filter:retweets AND -filter:replies")

# if we don't find tweets that include our tag then we search for general academic twitter hashtags 
search2  = ("#phdchat OR #academictwitter -filter:retweets AND -filter:replies")

running = True
while running == True:

    x = [1,2,3,4,5,6,7,8,9,10]
    random.shuffle(x)
    print("first element of x:", x[0])

    if x[0]<9:
        search_lists = [search1, search2]
        print(search_lists[0])
    else:
        search_lists = [search2, search1]
        print(search_lists[0])

    x=0
    y=0
    for tweet in tweepy.Cursor(api.search,
                                q=search_lists[0],
                                result_type="recent",
                                lang='en',
                                tweet_mode='extended').items(1):

        print("tweet 1 content: ", tweet.full_text)

        if tweet.user.screen_name in accounts_to_skip:
            print("Avoiding spam user: ", tweet.user.screen_name)
            break
        if tweet.full_text in accounts_to_skip:
            print("Avoiding spam user: ", tweet.user.screen_name)
            break

        if x==0:
            for account in accounts_to_skip:
                if account in tweet.full_text:
                    print("SPAM FOUND")
                    break

            if tweet.full_text.count("@") > 6:
                print("TOO MANY @ TAGS, SPAM ALERT")
                print("SPAM TWEET: ", tweet.full_text)
                break

            if tweet.full_text.count("#") > 6:
                print("TOO MANY HASH TAGS, SPAM ALERT")
                print("SPAM TWEET: ", tweet.full_text)
                break

            y+=1
            try:
                tweet.retweet()
                x+=1

            except tweepy.TweepError as e:
                print(e)
                if 'Failed to send request' in e.reason:
                    time.sleep(240)
            except StopIteration:
                break

        if x==0:
            print("second search..")
            y+=1
            for tweet in tweepy.Cursor(api.search,
                                        q=search_lists[1],
                                        result_type="recent",
                                        lang='en',
                                        tweet_mode='extended').items(1):

                print("tweet 2 content: ", tweet.full_text)

                if tweet.user.screen_name in accounts_to_skip:
                    print("Avoiding spam user: ", tweet.user.screen_name)
                    break
                    
                if tweet.full_text in accounts_to_skip:
                    print("Avoiding spam user: ", tweet.user.screen_name)
                    break

                if x==0:
                    print("username: ", tweet.user.screen_name)
                    print("tweet content is: ", tweet.full_text)

                    for account in accounts_to_skip:
                        if account in tweet.full_text:
                            print("SPAM FOUND")
                            break

                    if tweet.full_text.count("@") > 6:
                        print("TOO MANY @ TAGS, SPAM ALERT")
                        print("SPAM TWEET: ", tweet.full_text)
                        break

                    if tweet.full_text.count("#") > 6:
                        print("TOO MANY HASH TAGS, SPAM ALERT")
                        print("SPAM TWEET: ", tweet.full_text)
                        break
                try:
                    tweet.retweet()
                    x+=1
                    y+=1

                except tweepy.TweepError as e:
                    print(e)
                    if 'Failed to send request' in e.reason:
                        time.sleep(240)
                except StopIteration:
                    break
    # 2 searches but found nothing to share
    if y == 2:
        time.sleep(800)
        print("Completed two searches: nothing to share - sleeping for 600 seconds (10 mins)")
    # 2 searches and 1 share on the second search
    elif y==3:
        time.sleep(800)
        print("Completed two searches and found something to share on the second search - sleeping for 800 seconds (13 mins)")
    # 1 search and 1 share
    else:
        time.sleep(800)
        print("Completed one search and found @academicchatter / #academicchatter to share - sleeping for 800 seconds (13 mins)")