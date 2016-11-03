from TwitterSearch import *

import pandas as pd
from pandas import ExcelWriter

tweet_dict = {}

try:
    tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
    tso.set_keywords(['Hillary', 'Trump'])  # let's define all words we would like to have a look for
    tso.set_language('en')  # we want to see English tweets only
    tso.set_include_entities(True)  # and don't give us all those entity information

    # Please create a Twitter app key here https://apps.twitter.com
    ts = TwitterSearch(
        consumer_key='hjAiR0bG54BrCfoYo3sYg',
        consumer_secret='w73bFtBO02jswmjw3ln3jXqyZ9Bwwdslw6ZM1HIBKI',
        access_token='45871162-XX6R7StzotBFAIxHGGZkZ49GtoxdXFXpkmHi24ZqS',
        access_token_secret='gpOtpOaOrE9nUrfKu4OAIzqIIUsaRyboMqFDHWnKCRvan'
    )

    count = 1
    # iterate through the tweets
    for tweet in ts.search_tweets_iterable(tso):
        # print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))

        tweet_dict[count] = [str(tweet['id']), tweet['user']['screen_name'], tweet['text']]
        count = count + 1

    # print (tweet_dict)
    df = pd.DataFrame.from_dict(tweet_dict, orient='index')
    df.rename(columns={0: 'TweetID'}, inplace=True)
    df.rename(columns={1: 'User'}, inplace=True)
    df.rename(columns={2: 'Tweet'}, inplace=True)

    print(df)

except TwitterSearchException as e:  # take care of all those ugly errors if there are some
    print(e)

# save to xls

writer = ExcelWriter('tweets.xlsx')
df.to_excel(writer, 'Sheet1')
writer.save()