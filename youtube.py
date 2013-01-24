import os
import sys
API_KEY = os.environ.get('GOOGLE_API_KEY', None)

from apiclient.discovery import build
import json
import urllib
import httplib2

def get_video_info(video_id):
    if API_KEY is None:
        raise Exception('API key not found! Cannot proceed until this is set')

    # we should probably use the google api instead
    #yt_url = 'https://www.googleapis.com/youtube/v3/videos?%s' % urllib.urlencode(yt_params)
    #print yt_url
    yt = build('youtube', 'v3', http=httplib2.Http())
    req = yt.videos().list(part='snippet,topicDetails', key=API_KEY, id=video_id)
    if req != None:
        yt_json = req.execute()

    print yt_json
    if 'error' in yt_json.keys():
        print yt_resp
        return

    video_metadata = []
    if yt_resp and 'items' in yt_resp.keys() and len(yt_resp['items']) == 1:
        yt_vid = yt_resp['items'][0]
        topic_ids = yt_vid['topicDetails']['topicIds']

        freebase_params = { 'filter': '/common/topic/notable_for', 'key': API_KEY }
        qry_string = '%s&%s' % (urllib.urlencode(freebase_params), urllib.urlencode({'filter': '/type/object/type'}))
        song_title = None
        artist = None
        for tid in topic_ids:
            freebase_url = 'https://www.googleapis.com/freebase/v1/topic%s?%s' % (tid, qry_string)
            print freebase_url
            freebase_json = urllib.urlopen(freebase_url).read()

            freebase_resp = json.loads(freebase_json)
            freebase_name = freebase_resp['/type/object/name']['values'][0]['text']
            notable_for = freebase_resp['property']['/common/topic/notable_for']['values'][0]['text']
            if notable_for != 'Composition':
                song_title = freebase_name
            else:
                artist = freebase_name

            if song_title is not None and artist is not None:
                break

    print 'song=%s, artist=%s' % (song_title, artist)
    return

if __name__ == "__main__":
    get_video_info( sys.argv[1] )
