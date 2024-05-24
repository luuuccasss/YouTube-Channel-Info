from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Change 'YOUR_API_KEY' by your Youtube API KEY
API_KEY = 'YOUR_API_KEY'

def select_language():
    language = input("Choose language (Type 'EN' for English or 'FR' for French): ").upper()
    if language == 'EN':
        return 'EN'
    elif language == 'FR':
        return 'FR'
    else:
        print("Invalid language selection. Please choose either 'EN' or 'FR'.")
        return select_language()

def translate_message(message, language):
    translations = {
        'EN': {
            'enter_channel_name': "Enter the YouTube channel name: ",
            'channel_info': "Channel Information:",
            'subscribers': "Subscribers: ",
            'views': "Views: ",
            'latest_video': "Latest Video:",
            'title': "Title: ",
            'published_at': "Published at: ",
            'url': "URL: ",
            'no_video_found': "No video found.",
            'invalid_channel': "The specified channel does not exist or is inaccessible."
        },
        'FR': {
            'enter_channel_name': "Entrez le nom de la chaîne YouTube : ",
            'channel_info': "Informations sur la chaîne :",
            'subscribers': "Abonnés : ",
            'views': "Vues : ",
            'latest_video': "Dernière vidéo :",
            'title': "Titre : ",
            'published_at': "Publiée le : ",
            'url': "URL : ",
            'no_video_found': "Aucune vidéo trouvée.",
            'invalid_channel': "La chaîne spécifiée n'existe pas ou est inaccessible."
        }
    }
    return translations[language][message]

def search_channel(channel_name):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    try:
        request = youtube.search().list(
            part='snippet',
            q=channel_name,
            type='channel'
        )
        response = request.execute()

        if 'items' in response and response['items']:
            channel = response['items'][0]
            channel_id = channel['id']['channelId']
            return channel_id
    except HttpError as e:
        print(f"Error : {e}")
    return None

def get_channel_info(channel_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    try:
        request = youtube.channels().list(
            part='snippet, statistics',
            id=channel_id
        )
        response = request.execute()

        if 'items' in response:
            channel = response['items'][0]
            channel_title = channel['snippet']['title']
            subs_count = int(channel['statistics']['subscriberCount'])
            view_count = int(channel['statistics']['viewCount'])
            return channel_title, subs_count, view_count
    except HttpError as e:
        print(f"Error : {e}")
    return None, None, None

def get_latest_video_info(channel_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    try:
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            order='date',
            type='video'
        )
        response = request.execute()

        if 'items' in response and response['items']:
            latest_video = response['items'][0]
            video_title = latest_video['snippet']['title']
            video_published_at = latest_video['snippet']['publishedAt']
            video_url = f"https://www.youtube.com/watch?v={latest_video['id']['videoId']}"
            return video_title, video_published_at, video_url
        else:
            return None, None, None
    except HttpError as e:
        print(f"Error : {e}")
        return None, None, None

def format_number(number):
    return "{:,}".format(number)

def main():
    language = select_language()
    channel_name = input(translate_message('enter_channel_name', language))

    if channel_name:
        channel_id = search_channel(channel_name)

        if channel_id:
            channel_title, subs_count, view_count = get_channel_info(channel_id)
            if channel_title:
                print(f"\n{translate_message('channel_info', language)} '{channel_title}':")
                print(f"{translate_message('subscribers', language)} {format_number(subs_count)}")
                print(f"{translate_message('views', language)} {format_number(view_count)}")

                video_title, video_published_at, video_url = get_latest_video_info(channel_id)
                if video_title:
                    print(f"\n{translate_message('latest_video', language)}")
                    print(f"{translate_message('title', language)} {video_title}")
                    print(f"{translate_message('published_at', language)} {video_published_at}")
                    print(f"{translate_message('url', language)} {video_url}")
                else:
                    print(f"\n{translate_message('no_video_found', language)}")
            else:
                print(f"\n{translate_message('invalid_channel', language)}")
        else:
            print(f"\n{translate_message('invalid_channel', language)}")

if __name__ == "__main__":
    main()
