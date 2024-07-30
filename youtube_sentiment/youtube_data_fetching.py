import googleapiclient.discovery
from googleapiclient.errors import HttpError
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
from langdetect import detect, LangDetectException
from datetime import datetime, timedelta

# Set up YouTube Data API
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = ""

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

def search_videos(query, max_results=200):
    try:
        request = youtube.search().list(
            q=query,
            part="snippet",
            # order="relevance",
            maxResults=max_results
        )
        response = request.execute()
        
        videos = []
        for item in response['items']:
            if item['id']['kind'] == 'youtube#video':
                videos.append({
                    'videoId': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'publishedAt': item['snippet']['publishedAt']
                })
        return videos
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return []

def get_comments(video_id, video_title, language='en'):
    comments = []
    six_months_ago = datetime.now() - timedelta(days=180)
    
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
        )
        response = request.execute()
        
        while request:
            for item in response['items']:
                comment_snippet = item['snippet']['topLevelComment']['snippet']
                comment_text = comment_snippet['textOriginal']
                print(comment_snippet['publishedAt'])
                # comment_date = datetime.strptime(comment_snippet['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
                comment_date = datetime.strptime(comment_snippet['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")

                # detect language
                try: 
                    detected_language = detect(comment_text)
                except LangDetectException:
                    detected_language = None
                
                # if comment_date >= six_months_ago and 'neutrogena' in comment_text and detected_language == language:
                if comment_date >= six_months_ago and detected_language == language:
                    comments.append({
                        'Date': comment_date.strftime('%Y-%m-%d'),
                        'Title': video_title,
                        'Comment': comment_text,
                        'Url': f'https://www.youtube.com/watch?v={video_id}',
                        # 'videoID': video_id,
                        'Source': 'youtube',
                        'Language': detected_language,
                        # 'sentiment': ''
                    })
            
            if 'nextPageToken' in response:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    pageToken=response['nextPageToken'],
                    textFormat="plainText"
                )
                response = request.execute()
            else:
                break
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
    
    return comments

def create_dataframe(comments):
    df = pd.DataFrame(comments, columns=['Date', 'Title', 'Comment', 'Url', 'Source', 'Language'])
    return df

def create_sentiment(query):
  videos = search_videos(query)
  all_comments = []

  for video in videos:
    video_comments = get_comments(video['videoId'], video['title'])
    all_comments.extend(video_comments)

  result = create_dataframe(all_comments)
  return result

print(create_sentiment("neutrogena"))
