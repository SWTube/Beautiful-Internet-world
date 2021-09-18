import googleapiclient.discovery
import os

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyBWmr2Ep032sSE3PA7GKNa9caPletKXmRo"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.comments().list()
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()
