from flask import Flask, render_template
import random
import json
import urllib
import isodate
import os

API_KEY = os.environ["YOUTUBE_API_KEY"]

PLAYLISTS = [
    ("80's Hits", "PLCD0445C57F2B7F41"),
    ("90's Hits", "PL7DA3D097D6FDBC02"),
    ("2000's Hits", "PL05E1623111A9A860"),
    ("2005's Hits", "PLDxOJah-7k9vX6P5q6U2p5hckgjoEEV4e"),
    ("2009 Top 100", "PL5CC5DD240A19B742"),
    ("Classical", "PL3FF1C36D88A45765"),
    ]

app = Flask(__name__)

def cached(f):
    cache = {}
    def wrapped_function(*args):
        if args in cache:
            return cache[args]
        else:
            result = f(*args)
            cache[args] = result
            return result
    return wrapped_function

@cached
def get_video_info(video_id):
    """
    returns a dict with the important video metadata
    video_id is the part of the url in the youtube video
    """
    print "Getting video stuff"
    base_url = "https://www.googleapis.com/youtube/v3/videos"
    search_url= "{}?id={}&key={}&part=snippet,contentDetails".format(base_url, video_id, API_KEY)
    response = urllib.urlopen(search_url).read()
    data = json.loads(response)
    duration_string = data['items'][0]['contentDetails']['duration']
    duration_seconds = int(isodate.parse_duration(duration_string).total_seconds())
    title_string = data['items'][0]['snippet']['title']
    result_dict = {'duration': duration_seconds, 'name': title_string}
    return result_dict

@cached
def get_playlist_videos(playlist_id):
    """
    Returns a list of video_ids
    :param playlist_id: the part of the URL that identifies the youtube playlist
    e.g. https://www.youtube.com/playlist?list=PLCD0445C57F2B7F41
    the playlist_id is PLCD0445C57F2B7F41
    :return: list of video id strings
    """
    print "Getting playlist stuff"
    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    search_url = "{}?playlistId={}&key={}&part=snippet&maxResults=50".format(base_url, playlist_id, API_KEY)
    response = urllib.urlopen(search_url).read()
    data = json.loads(response)
    total_videos = data['pageInfo']['totalResults']

    video_list = []

    for video in data['items']:
        video_list.append(video['snippet']['resourceId']['videoId'])

    while len(video_list) < total_videos:
        next_token = data['nextPageToken']
        new_search_url = "{}&pageToken={}".format(search_url, next_token)
        response = urllib.urlopen(new_search_url).read()
        data = json.loads(response)
        for video in data['items']:
            video_list.append(video['snippet']['resourceId']['videoId'])

    return video_list

def video_url(video_id, time_start):
    """
    Returns the full youtube embed url, including the video_id
    and time_start which is given in seconds
    could eventually customize this with things like muted etc.
    """
    return "https://www.youtube.com/embed/{}?ecver=2&rel=0&autoplay=1&controls=0&modestbranding=1&&showinfo=0&start={}".format(video_id, time_start)

@app.route("/")
def index():
    return render_template("index.html", playlists=PLAYLISTS)

@app.route("/<playlist_id>")
def playlist(playlist_id):
    playlist = get_playlist_videos(playlist_id)
    video_id = random.choice(playlist)
    video_info = get_video_info(video_id)
    time_start = random.randint(10, video_info['duration'] - 20)
    youtube_link = video_url(video_id, time_start)

    return render_template("video.html", list_id=playlist_id,
                           youtubelink=youtube_link, videoname=video_info['name'], playlists=PLAYLISTS)

if __name__ == "__main__":
    app.run()
