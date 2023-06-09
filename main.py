import tweets_into_json
import Album_class
artist_name = input("Please enter an artist name: ")
album_name =  input("Please enter an album name: ")
album = Album_class.Album(album_name, artist_name)
tweets_into_json.main(album)