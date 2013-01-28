import os, re
from pyechonest import config, song
config.ECHO_NEST_API_KEY = os.environ.get('ECHO_NEST_API_KEY', None)

def get_from_echonest(title=None):
    if config.ECHO_NEST_API_KEY is None:
        raise Exception('ECHO_NEST_API_KEY variable cannot be None!')

    title = title_scrubber(title)
    title_parts = [t.strip() for t in title.split('-')]
    matches = song.search(title=title_parts[0], artist=title_parts[1])
    # try both ways, because we have no idea how people will
    # title the song in youtube
    if not matches:
        matches = song.search(title=title_parts[1], artist=title_parts[0])

    if not matches:
        return (None, None)
    else:
        match = matches[0]
        return (match.title, match.artist_name)

def title_scrubber(title):
    if '-' in title:
        return title

    by_idx = title.lower().find(' by ')
    if by_idx != -1:
        return '%s - %s' % (title[:by_idx], title[by_idx+len(' by '):])

    # match Etta James "At Last" (or "At Last" Etta James)
    match = re.match("(.{1,})?[\"|'](.{1,})[\"|'](.{1,})?", title)
    if match:
        if match.group(1):
            return "%s - %s" % (match.group(1), match.group(2))
        else:
            return "%s - %s" % (match.group(3), match.group(2))

    # TODO
    # how can i intelligenty switch 'At Last Etta James' with
    # 'Etta James At Last'?
    return title
