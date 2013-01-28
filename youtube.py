from apiclient import errors as apiclient_errors
from apiclient.discovery import build

from urlparse import urlparse, parse_qs
import json
import os
import re
import sys
import urllib
import gdata.youtube.service
from echonest import get_from_echonest

API_KEY = os.environ.get('GOOGLE_API_KEY', None)

def get_video_id(value):
    """
    Source: http://stackoverflow.com/a/7936523/117413
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    value = 'http://%s' % value if not value.startswith('http') else value
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

def get_video_info(video_id):
    if API_KEY is None:
        raise Exception('API key not found! Cannot proceed until this is set')

    song_title = None
    artist = None
    # v2 is just so much more reliable. Try this first, see if we get anything good
    yt_client = gdata.youtube.service.YouTubeService()
    vid_data = yt_client.GetYouTubeVideoEntry(video_id=video_id)
    title = vid_data.title.text
    song_title, artist = get_from_echonest(title)

    if song_title is None and artist is None:
        try:
            # try v3 first, just for fun.
            yt = build('youtube', 'v3')
            req = yt.videos().list(part='snippet,topicDetails', key=API_KEY, id=video_id)
            if req != None:
                yt_resp = req.execute()
                if yt_resp and 'items' in yt_resp.keys() and len(yt_resp['items']) == 1:
                    yt_vid = yt_resp['items'][0]
                    topic_ids = yt_vid['topicDetails']['topicIds']
                    song_title, artist = get_from_freebase(topic_ids)
        except apiclient_errors.HttpError, he:
            print 'HttpError: ', he
            pass

    return song_title, artist

def get_from_freebase(topic_ids):
    freebase_params = { 'filter': '/common/topic/notable_for', 'key': API_KEY }
    qry_string = '%s&%s' % (urllib.urlencode(freebase_params), urllib.urlencode({'filter': '/type/object/type'}))
    song_title = None
    artist = None
    for tid in topic_ids:
        freebase_url = 'https://www.googleapis.com/freebase/v1/topic%s?%s' % (tid, qry_string)
        print freebase_url
        freebase_json = urllib.urlopen(freebase_url).read()

        freebase_resp = json.loads(freebase_json)
        freebase_name = freebase_resp.get('/type/object/name')
        if not freebase_name:
            continue

        freebase_name = freebase_name['values'][0]['text']
        notable_for = freebase_resp['property']['/common/topic/notable_for']['values'][0]['text']
        if notable_for != 'Composition':
            song_title = freebase_name
        else:
            artist = freebase_name

        if song_title is not None and artist is not None:
            break
    return song_title, artist


if __name__ == "__main__":
    url = 'www.youtube.com/watch?v=D9JOxagV9Pw' if len(sys.argv) == 1 else sys.argv[1]

    vid_id = get_video_id(url)
    print get_video_info( vid_id )
