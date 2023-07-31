import time
import requests
import pandas as pd
import os

API_KEY = os.environ.get('YOUTUBE_API_KEY')

def get_videos_with_keyword(keyword, TOTAL_VIDEOS, MAX_RESULTS_PER_PAGE, DELAY_BETWEEN_REQUESTS):
    videos = []
    next_page_token = None

    while len(videos) < TOTAL_VIDEOS:
        url = f'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part': 'snippet',
            'q': keyword,
            'type': 'video',
            'key': API_KEY,
            'maxResults': min(MAX_RESULTS_PER_PAGE, TOTAL_VIDEOS - len(videos)),
            'pageToken': next_page_token
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            videos.extend(data['items'])
            next_page_token = data.get('nextPageToken')
        else:
            print('Wystąpił błąd podczas pobierania danych.')
            print('Kod odpowiedzi:', response.status_code)
            print(response)
            break

        if not next_page_token:
            break

        # delay between requests
        time.sleep(DELAY_BETWEEN_REQUESTS)

    return videos



def get_video_statistics(video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'statistics',
        'id': video_id,
        'key': API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['items'][0]['statistics']
    else:
        print('Wystąpił błąd podczas pobierania danych.')
        print('Kod odpowiedzi:', response.status_code)
        return {}
