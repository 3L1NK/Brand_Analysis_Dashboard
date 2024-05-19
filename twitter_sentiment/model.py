import tweepy

# Replace with your own credentials
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

hashtag = '#YourBrand'
tweets = tweepy.Cursor(api.search_tweets, q=hashtag, lang="en").items(100)

tweet_texts = [tweet.text for tweet in tweets]

from textblob import TextBlob

for tweet in tweet_texts:
    analysis = TextBlob(tweet)
    print(f'Tweet: {tweet}\nSentiment: {analysis.sentiment}\n')

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

for tweet in tweet_texts:
    vs = analyzer.polarity_scores(tweet)
    print(f'Tweet: {tweet}\nSentiment: {vs}\n')

import matplotlib.pyplot as plt

sentiments = [analyzer.polarity_scores(tweet)['compound'] for tweet in tweet_texts]

plt.hist(sentiments, bins=20)
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.title('Sentiment Analysis of #YourBrand')
plt.show()