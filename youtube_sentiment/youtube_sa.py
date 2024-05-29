
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from textblob import TextBlob
import matplotlib.pyplot as plt

# Set up YouTube Data API
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyAMVbpj1t3zoXDLcZYBRp_i8hrt8uAn_JY"

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

# Function to get comments for a specific video
def get_video_comments(video_id, max_results=50):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText"
    )
    try:
        response = request.execute()
    except HttpError as e:
        if e.resp.status == 403:
            error_details = e.error_details
            for detail in error_details:
                if detail.get('reason') == 'commentsDisabled':
                    print(f"Comments are disabled for video: {video_id}")
                    return comments
        else:
            raise e

    while request and len(comments) < max_results:
        for item in response['items']:
            comments.append(item['snippet']['topLevelComment']['snippet']['textOriginal'])
        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=max_results - len(comments),
                pageToken=response['nextPageToken'],
                textFormat="plainText"
            )
            response = request.execute()
        else:
            break
    
    return comments

# Function to search videos by query and get comments
def get_comments_by_query(query, max_results=50):
    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=max_results,
        type="video"
    )
    response = request.execute()

    all_comments = []
    for item in response['items']:
        video_id = item['id']['videoId']
        comments = get_video_comments(video_id, max_results // len(response['items']))
        all_comments.extend(comments)
    
    return all_comments

# Function to analyze sentiment of comments
def analyze_sentiment(comments):
    polarity = []
    for comment in comments:
        analysis = TextBlob(comment)
        polarity.append(analysis.sentiment.polarity)
    return polarity

# Queries for each brand
queries = {
    "Copilot by Microsoft": "Microsoft Copilot AI",
    "ChatGPT by OpenAI": "OpenAI ChatGPT",
    "Gemini by Google": "Google Gemini AI"
}

# Get comments and analyze sentiment
brand_sentiments = {}
for brand, query in queries.items():
    comments = get_comments_by_query(query)
    sentiment = analyze_sentiment(comments)
    brand_sentiments[brand] = sentiment

# Plotting the results
plt.figure(figsize=(12, 6))
for brand, sentiment in brand_sentiments.items():
    plt.hist(sentiment, bins=30, alpha=0.5, label=brand)

plt.title('Sentiment Analysis of YouTube Comments for AI Chat Technologies')
plt.xlabel('Sentiment Polarity')
plt.ylabel('Number of Comments')
plt.legend(loc='upper left')
plt.show()
