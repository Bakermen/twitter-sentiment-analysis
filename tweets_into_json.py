import additional_functions as af
import tweepy as tw
from dotenv import load_dotenv
import json
import os
from datetime import datetime


load_dotenv

api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")
access_token = os.getenv("access_token")
token_secret = os.getenv("token_secret")


auth = tw.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, token_secret)
api = tw.API(auth)

def album_exists(album):
    if(not(af.get_album_release_date(album.artist_name, album.album_name))):
        return False
    return True

"""""""""""""""""""""""""""
This function will take an album object and fetch tweets based on the album and the artist name,
then it will turn the tweets into readable data and return them as a dictionary.
"""""""""""""""""""""""""""

def get_tweets(album):
    #we will use the album name and the artist name as keywords
    key_word = album.album_name + ' ' + album.artist_name

    #searches the album in spotify database
    if(not album_exists(album)):
        print("couldn't find album.")
        return

    release_date = album.get_release_date()

    # start fetching tweets a week before the album was released
    starting_date = datetime(release_date.year, release_date.month, release_date.day-7)

    tweets = []
    main_dict = {}

    #needed variables to stop the run if there are no new tweets
    main_dict_count = len(main_dict) 
    duplicate_count = 0
    
    #needed variable to store the id of the last tweete fetched
    last_id = None

    #maximum number of tweets fetched
    tweets_count =200

    print('fetching tweets...')
    while len(main_dict) < tweets_count:
        count = 50 #900 tweets fetched at a time
        new_tweets = tw.Cursor(api.search, q = key_word, lang = 'en', max_id = last_id, since= starting_date).items(count)

        #will stop the run if there are no new tweets fetched
        if not new_tweets:
            print("that's as much tweets as we could gather.")
            break

        #will add the tweets to the main array of tweets
        tweets.extend(new_tweets)

        #handleing the error if there was an album but the api couldn't find any tweets for it
        try:
            last_id = tweets[-1].id-1
        except:
            print("couldn't find any tweets on the album.")
            break

        #turns the tweet objects into readable data and puts them in a dictionary
        for tweet in tweets:
            if len(main_dict) == tweets_count:
                break
            main_dict.update({
                tweet.id_str:{
                    'user_id': tweet.user.id,
                    'text': tweet.text,
                    'likes': tweet.favorite_count,
                    'retweets': tweet.retweet_count,
                } 
            })

        #starts counting if the total number of tweets was the same after fetching 
        if(len(main_dict) == main_dict_count):
            duplicate_count +=1
        else:
            duplicate_count = 0

        #if the total number of tweets is the same after fetching 5 times it will stop fetching
        if(duplicate_count >=4):
            print("that's as much tweets as we could gather.")
            break

        main_dict_count = len(main_dict)

        print('gathered ', len(main_dict), '/', tweets_count,' tweets')

        # waits 15 minutes before the loop starts again, because of the fetching cap
        # time.sleep(900)

        new_tweets = []
        
    if(len(main_dict) == 0):
        return

    print('done fetching.')
    return main_dict
        
def make_json(album_dict, json_name):
    print('making the json file...')
    with open("jsons/%s.json"%json_name, 'a+') as file:
        json.dump(album_dict, file, indent= 4)

def main(album):
    tweets = get_tweets(album)
    #will remove all the punctuations from the album and artist name to properly make the json file
    purified = album.purify_names()

    #will make the json file if there are any tweets
    if(tweets):
        make_json(tweets, purified.artist_name +'-'+purified.album_name)