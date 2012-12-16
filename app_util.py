
def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['mp3', 'mp4', 'wav', 'm4a', 'ogg'])
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
