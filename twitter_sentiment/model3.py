import tweepy

# Replace with your own credentials
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAJudtwEAAAAAyeYEb6xDQFv83R1eX0nFdz9lKw8%3DHN5fOyrGGaZE4uGvvIugi0uT1ijeNzpmePtn6KPECQD7o8ASJF'

# Initialize tweepy Client with bearer token
client = tweepy.Client(bearer_token=bearer_token)

# Define the query
query = '#ChatGPT lang:en'

# Fetch tweets using tweepy.Client.search_recent_tweets
tweets = client.search_recent_tweets(query=query, max_results=5, tweet_fields=['text'])

# Extract tweet texts
tweet_texts = [tweet.text for tweet in tweets.data]

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
plt.title('Sentiment Analysis of #ChatGPT')
plt.show()
