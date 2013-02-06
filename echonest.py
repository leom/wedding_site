import os, re
from pyechonest import config, song
from config import Config as AppConfig
config.ECHO_NEST_API_KEY = AppConfig.ECHO_NEST_API_KEY

def get_from_echonest(title=None):
    if config.ECHO_NEST_API_KEY is None:
        raise Exception('ECHO_NEST_API_KEY variable cannot be None!')

    title_parts = title_splitter(title)
    if len(title_parts) == 0 or title_parts[1] is None:
        title_parts = title.split(' ')

    for (i, ignored) in enumerate(title_parts):
        word1 = ' '.join(title_parts[0:i+1])
        word2 = ' '.join(title_parts[i+1:])
        matches = song.search(title=word1, artist=word2)
        if matches:
            break
        matches = song.search(title=word2, artist=word1)
        if matches:
            break
        #matches = song.search(title=title_parts[0], artist=title_parts[1])
        #if not matches:
        #    matches = song.search(title=title_parts[1], artist=title_parts[0])

    if not matches:
        return (None, None)
    else:
        match = matches[0]
        return (match.title, match.artist_name)

def title_splitter(title):
    title = title_scrubber(title)
    title_parts = [t.strip() for t in title.split('-')]
    if not title_parts or len(title_parts) != 2:
        title_parts = (title, None)
    return title_parts

def title_scrubber(title):
    if '[video]' in title.lower():
        vid_re = re.compile('\[\s*Video\s*\]', re.IGNORECASE)
        title = vid_re.sub('', title)

    if '-' in title:
        return title

    if title.count(',') == 1:
        return title.replace(',', ' - ')

    by_idx = title.lower().find(' by ')
    if by_idx != -1:
        return '%s - %s' % (title[:by_idx], title[by_idx+len(' by '):])

    match = re.match("(.{1,})?[\"|'](.{1,})[\"|'](.{1,})?", title)
    if match:
        if match.group(1):
            return "%s - %s" % (match.group(1), match.group(2))
        else:
            return "%s - %s" % (match.group(3), match.group(2))
    return title
