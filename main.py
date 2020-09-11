import tweepy
import preprocessor as p
from textblob import TextBlob
import os


consumer_key = os.environ.get('TWITTER_API_KEY')
consumer_secret = os.environ.get('TWITTER_API_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_secret = os.environ.get('TWITTER_ACCESS_SECRET')


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


def get_tweets(keyword):
    '''fetches tweets related to a keyword/ hashtag'''

    # tweet_iter returns an iterator. Each item in the iterator has various attributes (text, username, date and more)
    tweet_iter = tweepy.Cursor(api.search, q=keyword, lang='en').items(10)

    tweets = [tweet.text for tweet in tweet_iter]

    return tweets


def clean_tweets(tweets):
    '''cleans the tweets gathered by the get tweets function'''

    cleaned_tweets = [p.clean(tweet) for tweet in tweets]

    return cleaned_tweets


def analyse_sentiment(cleaned_tweets):
    '''analyses the sentiment of tweets returned by the clean tweets function'''
    sentiment_score = []
    for tweet in cleaned_tweets:
        blob = TextBlob(tweet)
        sentiment_score.append(blob.sentiment.polarity)

    # returns the mean sentiment score
    return sum(sentiment_score)/len(sentiment_score)


print('What do people prefer more: \n')
hashtag1 = '#' + input()
print('OR... \n')
hashtag2 = '#' +input()

get_hashtag1 = get_tweets(hashtag1)
clean_hashtag1 = clean_tweets(get_hashtag1)
sentiment_hashtag1 = analyse_sentiment(clean_hashtag1)

get_hashtag2 = get_tweets(hashtag2)
clean_hashtag2 = clean_tweets(get_hashtag2)
sentiment_hashtag2 = analyse_sentiment(clean_hashtag2)

if sentiment_hashtag1 > sentiment_hashtag2:
    print(f'{hashtag1} is preferred more!')
else:
    print(f'{hashtag2} is preferred more')
