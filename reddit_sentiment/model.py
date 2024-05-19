import praw

# Replace with your own credentials
reddit = praw.Reddit(client_id='your_client_id',
                     client_secret='your_client_secret',
                     user_agent='your_user_agent')

subreddit_name = 'YourSubreddit'
subreddit = reddit.subreddit(subreddit_name)

posts = subreddit.search('YourBrand', limit=100)
comments = []
for post in posts:
    post.comments.replace_more(limit=0)
    for comment in post.comments.list():
        comments.append(comment.body)

print(comments[:5])  # Display first 5 comments

from textblob import TextBlob

for comment in comments:
    analysis = TextBlob(comment)
    print(f'Comment: {comment}\nSentiment: {analysis.sentiment}\n')

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

for comment in comments:
    vs = analyzer.polarity_scores(comment)
    print(f'Comment: {comment}\nSentiment: {vs}\n')

import matplotlib.pyplot as plt

sentiments = [analyzer.polarity_scores(comment)['compound'] for comment in comments]

plt.hist(sentiments, bins=20)
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.title('Sentiment Analysis of YourBrand on Reddit')
plt.show()