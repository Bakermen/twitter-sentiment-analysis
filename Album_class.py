import string
import additional_functions as af


class Album:
    def __init__(self, album_name, artist_name):
        self.album_name = album_name.lower()
        self.artist_name = artist_name.lower()
    
    def purify_names(self):
        purified_album = Album('', '')
        purified_album.album_name = self.album_name.translate(str.maketrans('', '', string.punctuation))
        purified_album.artist_name = self.artist_name.translate(str.maketrans('', '', string.punctuation))
        return purified_album
    
    def get_release_date(self):
        return af.get_album_release_date(self.artist_name, self.album_name)