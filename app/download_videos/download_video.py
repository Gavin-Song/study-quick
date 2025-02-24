import pytube
import os
import datetime
import json
import sys


def get_video_id(video_url):
    yt = pytube.YouTube(video_url)
    video_data = yt.player_config_args.get('player_response').get('videoDetails')
    video_id = video_data['videoId']

    return video_id, yt


def download_video(video_url):
    video_id, yt = get_video_id(video_url)

    # Try finding captions to test if video is valid
    caption = yt.captions.get_by_language_code("en") or yt.captions.all()[0]
    caption_list = caption.generate_srt_captions().splitlines()

    if os.path.exists('./public/saves/' + video_id):
        return yt, video_id, {}

    video = yt.streams.filter(progressive=True) \
        .order_by('resolution') \
        .desc() \
        .first()

    video_data = yt.player_config_args.get('player_response').get('videoDetails')
    video_title = video_data['title']
    video_author = video_data['author']
    video_length_in_seconds = video_data['lengthSeconds']
    video_length_formatted = str(datetime.timedelta(seconds=int(video_length_in_seconds)))

    newpath = './public/saves/' + video_id
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    video.download('./public/saves/' + video_id, 'temp')

    meta_data = {'video_id': video_id, 'video_title': video_title, \
                'video_author': video_author, 'video_length': video_length_formatted}

    output_file = 'meta_data.json'
    with open('./public/saves/' + video_id + '/' + output_file, 'w') as f:
        json.dump(meta_data, f)
    return yt, video_id, meta_data

