
import requests
from requests_oauthlib import OAuth1
#from sqlite3 import dbapi2 as sqlite3
import json
import logging
import time , codecs, urllib
import ConfigParser
from models import Posts

logging.basicConfig(filename='fetcher.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


class Fetcher:

    search_terms = []

    def __init__(self):
        Config = ConfigParser.ConfigParser()
        Config.readfp(codecs.open('config.ini', 'r', 'utf8'))

        key = Config.get('Twitter', 'key')
        secret = Config.get('Twitter', 'secret')
        token = Config.get('Twitter', 'token')
        token_secret = Config.get('Twitter', 'token_secret')
        self.search_terms = Config.get('Search_Terms', 'search_terms').split(',')
        self.auth = OAuth1(key, secret, token, token_secret)

    def getTweetsJSON(self, term):
        # Aslak had commented this out - not sure what it was supposed to do
        #since = ''
        #lastTweetID = self.getHighID()
        #if lastTweetID:
        #    since = '&since_id={0}'.format(lastTweetID)

        search_url =  u'https://api.twitter.com/1.1/search/tweets.json?q={0}&result_type=recent&count=100'
        search_url = search_url.format(term)
        resp = requests.get(search_url, auth=self.auth)
        if resp.status_code == 200:
            logging.info("yay, 200 response")
            return json.loads(resp.text)
        else:
            logging.warning("{0} - {1}".format(resp.status_code, resp.text))
            return None


    def getHighID(self):
        pass


    def hasTweet(self, tweetID):
        pass 


    def saveTweets(self, term):
        tweets = self.getTweetsJSON(term)
        return
        if not tweets:
            logging.info("Saved 0 tweets")
            return 0
            
        for tweet in tweets['statuses']:

            # Discard retweets
            if tweet.has_key('retweeted_status'):
                continue

            post = Posts()

            if not post.hasPost(tweet['id']):

                post.orig_post_id = int(tweet['id'])
                post.orig_user_id = int(tweet['user']['id'])
                post.date = int(time.mktime(time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')))
                post.username = tweet['user']['screen_name']
                post.text = tweet['text']
                post.image_small = [tweet['entities']['media'][0]['media_url'] if 'media' in tweet['entities'] else ''][0]
                post.image_full = [tweet['entities']['media'][0]['media_url'] if 'media' in tweet['entities'] else ''][0]
                post.service = 'twitter'
                post.likes = None
                post.orig_url = None
                
                post.save()
            

if __name__ == "__main__":
    f = Fetcher()
    for term in f.search_terms:
        f.saveTweets(term)

