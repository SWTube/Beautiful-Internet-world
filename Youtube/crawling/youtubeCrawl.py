from google.colab import files
import google_auth_oauthlib.flow
import googleapiclient.discovery

#------------------------------------------------------------------------------------------------#

uploaded = files.upload()

#------------------------------------------------------------------------------------------------#  

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRET_FILE = 'client_secret_850373388747-p2ov8rimve759a2vq62sjjkbrmenijgb.apps.googleusercontent.com.json'

# [ 사용할 권한 명시 ]
# 1. 유튜브 계정 보기(youtube.readonly)
# 2. 유튜브 동영상, 평가, 댓글, 자막 보기, 수정 및 완전 삭제(youtube.force-ssl)
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly', 'https://www.googleapis.com/auth/youtube.force-ssl']

# API 클라이언트 생성 및 인증하여 Credential 객체 얻기
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

#------------------------------------------------------------------------------------------------#

# 인증된 사용자 채널의 기본 정보 가져오기
channels_response = youtube.channels().list(
    mine=True,
    part='contentDetails'
).execute()

channel = channels_response['items'][0] # 첫 번째 채널 선택
uploads_playlist_id = channel['contentDetails']['relatedPlaylists']['uploads'] # 업로드 영상 플레이 리스트 ID 추출

print('업로드한 영상의 Playlist ID:', uploads_playlist_id)

#------------------------------------------------------------------------------------------------#

# 인증된 사용자 채널의 모든 비디오 정보 가져오기
playlistitems_list_request = youtube.playlistItems().list(
    playlistId=uploads_playlist_id,
    part='snippet',
    maxResults=50
)

cnt = 0
last = 20 # 최근 몇 개까지의 동영상을 확인할지 설정
video_list = []

# 해당 플레이 리스트의 모든 동영상을 하나씩 확인하며
while playlistitems_list_request:
    playlistitems_list_response = playlistitems_list_request.execute()

    # 각 비디오(video)에 대한 정보 출력
    for playlist_item in playlistitems_list_response['items']:
        video_id = playlist_item['snippet']['resourceId']['videoId']
        title = playlist_item['snippet']['title']
        video_list.append((video_id, title))
        cnt += 1
        if cnt >= last:
            break

    if cnt >= last:
        break
    playlistitems_list_request = youtube.playlistItems().list_next(playlistitems_list_request, playlistitems_list_response)

print('{cnt}개의 동영상 정보를 불러왔습니다.')

#------------------------------------------------------------------------------------------------#

for (video_id, title) in video_list:
    print('Video ID: {video_id} / 제목: {title}')

#------------------------------------------------------------------------------------------------#

# commentThreads.list() API를 호출하여 특정 비디오의 댓글 스레드(thread)를 불러오기
def get_comment_threads(youtube, video_id):
    results = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100, # 최근 100개까지의 댓글 확인
    ).execute()

    comment_list = []
    for item in results['items']:
        comment_id = item['id']
        comment = item['snippet']['topLevelComment']
        author = comment['snippet']['authorDisplayName']
        publishedAt = comment['snippet']['publishedAt']
        text = comment['snippet']['textDisplay']
        comment_list.append((comment_id, author, publishedAt, text))

    return comment_list

#------------------------------------------------------------------------------------------------#

video_id = 'ukkLCl9yBvE' # 비디오 ID
comment_list = get_comment_threads(youtube, video_id)

for (comment_id, author, publishedAt, text) in comment_list:
    print('[ Comment ID: {comment_id} / 작성자: {author} / 작성 날짜: {publishedAt} ]')
    print(text)

#------------------------------------------------------------------------------------------------#

comment_ids = ['Ugzk1Ct6DqtrHjxHl5N4AaABAg', 'UgyEeP3bVrIH6smvlsl4AaABAg'] # 댓글 ID 설정
banned = True # 댓글 작성자 차단 여부

# 삭제 수행 (삭제 이후에는 더 이상 API 상에서도 해당 댓글이 보이지 않음)
request = youtube.comments().setModerationStatus(
    id=comment_ids,
    moderationStatus='rejected',
    banAuthor=banned
)
request.execute()

print(len(comment_ids), '개의 댓글을 삭제했습니다.')

#------------------------------------------------------------------------------------------------#

comment_ids = ['Ugzk1Ct6DqtrHjxHl5N4AaABAg', 'UgyEeP3bVrIH6smvlsl4AaABAg'] # 댓글 ID 설정
banned = False # 댓글 작성자 차단 여부

# 다시 보이게 만들기 (댓글 ID를 기억하고 있는 경우에는 다시 보이게 만들 수 있음)
request = youtube.comments().setModerationStatus(
    id=comment_ids,
    moderationStatus='published',
    banAuthor=banned
)
request.execute()

print(len(comment_ids), '개의 댓글을 복구했습니다.')