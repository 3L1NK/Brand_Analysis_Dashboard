import tweepy
from tweepy import TweepyException
import pandas as pd
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns

# Twitter API credentials
# consumer_key = 'FV3FC3OOojtWgAqrdDXVwvBlk'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAJudtwEAAAAAyeYEb6xDQFv83R1eX0nFdz9lKw8%3DHN5fOyrGGaZE4uGvvIugi0uT1ijeNzpmePtn6KPECQD7o8ASJF'
# consumer_secret = 'RW97oqiCzPtKn7FPzwsQXhPwGLQDDfbuGHHnArdrxUZMLtoeAN'
# access_token = '1791398915113205760-obLLCohz2A2qN0xzkTag9nAibDNQre'
# access_token_secret = 'CPP7DKKcBI3zwtl2wjMBy4HbdbaAdvXxuNghHKgPA4u9I'

new_bearer ='AAAAAAAAAAAAAAAAAAAAAJudtwEAAAAAXG3c877e7NB%2BzU%2B0OKeIiib7vtc%3DdMZkXDm2FwjFCl38VUXTetQ9sOFk2A3C0v5sPRHD8rYJhfRcNd'

# Authenticate to the Twitter API v2
# client = tweepy.Client(bearer_token=bearer_token)


print('connecting')
print(client)

# Function to fetch tweets using Twitter API v2
def fetch_tweets_v2(query, max_results=100):
    try:
        tweets = client.search_recent_tweets(query=query, tweet_fields=['created_at', 'author_id', 'text'], max_results=max_results)
        tweet_list = [[tweet.created_at, tweet.author_id, tweet.text] for tweet in tweets.data]
        return pd.DataFrame(tweet_list, columns=["Date", "User", "Tweet"])
    except TweepyException as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame(columns=["Date", "User", "Tweet"])

# Function to clean tweets
def clean_tweet(tweet):
    tweet = re.sub(r'http\S+', '', tweet)
    tweet = re.sub(r'@\w+', '', tweet)
    tweet = re.sub(r'#\w+', '', tweet)
    tweet = re.sub(r'\s+', ' ', tweet)
    tweet = re.sub(r'[^\w\s]', '', tweet)
    return tweet

# Sentiment analysis with TextBlob
def get_sentiment_textblob(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

# Sentiment analysis with VADER
analyzer = SentimentIntensityAnalyzer()

def get_sentiment_vader(tweet):
    vs = analyzer.polarity_scores(tweet)
    if vs['compound'] > 0:
        return 'Positive'
    elif vs['compound'] == 0:
        return 'Neutral'
    else:
        return 'Negative'

# Fetch, clean, analyze, and visualize tweets for multiple brands
def analyze_brands(brands):
    df_list = []
    for brand in brands:
        df = fetch_tweets_v2(brand, 100)
        df['Brand'] = brand
        df['Cleaned_Tweet'] = df['Tweet'].apply(clean_tweet)
        df['Sentiment_TextBlob'] = df['Cleaned_Tweet'].apply(get_sentiment_textblob)
        df['Sentiment_VADER'] = df['Cleaned_Tweet'].apply(get_sentiment_vader)
        df_list.append(df)
    
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Visualization
    sns.countplot(x='Sentiment_TextBlob', hue='Brand', data=combined_df)
    plt.title('Sentiment Analysis using TextBlob')
    plt.show()

    sns.countplot(x='Sentiment_VADER', hue='Brand', data=combined_df)
    plt.title('Sentiment Analysis using VADER')
    plt.show()

    combined_df['Date'] = pd.to_datetime(combined_df['Date']).dt.date
    sentiment_time_series = combined_df.groupby(['Date', 'Brand', 'Sentiment_TextBlob']).size().unstack()
    sentiment_time_series.plot(kind='line', figsize=(12, 6))
    plt.title('Sentiment Analysis Over Time (TextBlob)')
    plt.show()

    sentiment_time_series_vader = combined_df.groupby(['Date', 'Brand', 'Sentiment_VADER']).size().unstack()
    sentiment_time_series_vader.plot(kind='line', figsize=(12, 6))
    plt.title('Sentiment Analysis Over Time (VADER)')
    plt.show()

# Main function to compare sentiment for Nike, Adidas, and Puma
if __name__ == "__main__":
    brands = ['ChatGPT', 'Gemini', 'Copilot']
    analyze_brands(brands)