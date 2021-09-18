import pandas
from googleapiclient.discovery import build

# YOUTUBEAPI, VIDEOID만 수정하면 바로 동작합니다.
# get Google Youyube Api key : https://console.cloud.google.com/apis/dashboard

comments = list()
api_obj = build('youtube', 'v3', developerKey = YOUTUBEAPI)
response = api_obj.commentThreads().list(part='snippet,replies', videoId=VIDEOID, maxResults=100).execute() #videoID is video's Only code

while response:
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append([comment['textDisplay'], comment['authorDisplayName'], comment['publishedAt'], comment['likeCount']])
 
        if item['snippet']['totalReplyCount'] > 0:
            for reply_item in item['replies']['comments']:
                reply = reply_item['snippet']
                comments.append([reply['textDisplay'], reply['authorDisplayName'], reply['publishedAt'], reply['likeCount']])
 
    if 'nextPageToken' in response:
        response = api_obj.commentThreads().list(part='snippet,replies', videoId=VIDEOID, pageToken=response['nextPageToken'], maxResults=100).execute() #videoID is video's Only code
    else:
        break

df = pandas.DataFrame(comments)
df.to_excel('results.xlsx', header=['comment', 'author', 'date', 'num_likes'], index=None)

