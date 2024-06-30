import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import re 

# Define a function to clean the comments
def clean_comment(comment):
    # Remove URLs
    comment = re.sub(r'http\S+', '', comment)
    # Remove non-alphabetic characters and convert to lowercase
    comment = re.sub(r'[^A-Za-z\s]', '', comment).lower()
    return comment

# Load the CSV file
#file_path = './reddit_sentiment/neutrogena_reddit.csv'
df1 = pd.read_csv('./reddit_sentiment/neutrogena_reddit.csv')
df2 = pd.read_csv('./youtube_sentiment/youtube_comments_with_sentiment.csv')

df = pd.concat([df1, df2], ignore_index=True)
df['Cleaned_Comment'] = df['Comment'].apply(clean_comment)

# Define additional stop words
additional_stopwords = {"skin", "product", "https", "use", "one", "would", "like", "get"}


# Filter comments based on sentiment
positive_comments = " ".join(comment for comment in df[df.Sentiment == 'positive'].Cleaned_Comment)
neutral_comments = " ".join(comment for comment in df[df.Sentiment == 'neutral'].Cleaned_Comment)
negative_comments = " ".join(comment for comment in df[df.Sentiment == 'negative'].Cleaned_Comment)

# Generate the word clouds
positive_wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Blues', stopwords=STOPWORDS.union(additional_stopwords)).generate(positive_comments)
neutral_wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Greys', stopwords=STOPWORDS.union(additional_stopwords)).generate(neutral_comments)
negative_wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Reds', stopwords=STOPWORDS.union(additional_stopwords)).generate(negative_comments)

# Display the word clouds
fig, ax = plt.subplots(1, 3, figsize=(20, 10))

# Positive words cloud
ax[0].imshow(positive_wordcloud, interpolation='bilinear')
ax[0].set_title('Positive Sentiment', fontsize=20)
ax[0].axis('off')

# Neutral words cloud
ax[1].imshow(neutral_wordcloud, interpolation='bilinear')
ax[1].set_title('Neutral Sentiment', fontsize=20)
ax[1].axis('off')

# Negative words cloud
ax[2].imshow(negative_wordcloud, interpolation='bilinear')
ax[2].set_title('Negative Sentiment', fontsize=20)
ax[2].axis('off')
plt.show()
