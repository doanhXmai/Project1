# track_title
# track_poster
# track_info
# track_uploader_date
# track_uploader_user_id
# track_duration
# track_audio
# track_officialAlbum
from fastapi import UploadFile, File, Form

class UploadTrackRequest:
    def __init__(self,
                 track_title: str = Form(...),
                 track_poster: UploadFile = File(None),
                 track_info: str = Form(None),
                 track_audio: UploadFile = File(...),
                 track_official_album: str = Form(None)
        ):
        self.track_title = track_title
        self.track_poster = track_poster
        self.track_info = track_info
        self.track_audio = track_audio
        self.track_officialAlbum = track_official_album
