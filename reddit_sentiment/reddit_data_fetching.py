#!pip install praw transformers torch
import praw
import pandas as pd
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import matplotlib.pyplot as plt
import seaborn as sns
import re
from datetime import datetime, timedelta
from langdetect import detect, LangDetectException


def fetch_reddit_comments(subreddit, query, limit=100, months=6):
    subreddit = reddit.subreddit(subreddit)
    posts = []
    for post in subreddit.search(query, limit=limit):
        post_date = datetime.utcfromtimestamp(post.created_utc)
        post.comments.replace_more(limit=0)  # Ensure all comments are fetched
        comments = post.comments.list()
        if comments:
            for comment in comments:
                if hasattr(comment, 'body') and comment.body.strip():  # Ensure comment body is not empty or just whitespace
                    try:
                        comment_date = datetime.utcfromtimestamp(comment.created_utc)
                        if detect(comment.body) == 'en' and comment_date >= datetime.now() - timedelta(days=months*30):  # Adjust to the specific time frame
                            posts.append([comment_date, post.title, comment.body, post.url])
                            english = True
                    except LangDetectException:  # Handle cases where language detection fails
                        continue

    df = pd.DataFrame(posts, columns=["Date", "Title", "Comment", "Url"])
    df['Date'] = pd.to_datetime(df['Date'], unit='s')
    df['Source'] = 'Reddit'
    if english == True: 
        df['Language'] = 'English'
    return df

def truncate_text(text, max_tokens=510):
    tokens = tokenizer.tokenize(text)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    return tokenizer.convert_tokens_to_string(tokens)

def get_sentiment_score(text):
    truncated_text = truncate_text(text)
    result = sentiment_pipeline(truncated_text)[0]
    return result['label'], result['score']

# Apply sentiment analysis

if __name__ == '__main__':
    user_agent = "Brand sentiment analysis"
    reddit = praw.Reddit(
    client_id="ujQpmAa-rxhI6tgE246E4w",
    client_secret="BnhybdI_fallhH64Us6vutIfsXP21Q",
    user_agent=user_agent
    )
    df = fetch_reddit_comments('all', 'apple', 100)
    

    # Load sentiment analysis pipeline
    #model_name = "distilbert-base-uncased-finetuned-sst-2-english" #only pos and neg
    model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    sentiment_pipeline = pipeline("sentiment-analysis", model=model_name)

    df['Sentiment'], df['Sentiment_Score'] = zip(*df['Comment'].apply(get_sentiment_score))
    # Convert the 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Group by week / day and sentiment
    df['Week'] = df['Date'].dt.to_period('W').apply(lambda r: r.start_time)
    weekly_sentiment = df.groupby(['Week', 'Sentiment']).size().unstack(fill_value=0)
    df['Day'] = df['Date'].dt.to_period('D').apply(lambda r: r.start_time)
    daily_sentiment = df.groupby(['Day', 'Sentiment']).size().unstack(fill_value=0)

    df.to_csv('./apple_reddit.csv', sep=',', index=False, encoding='utf-8')

