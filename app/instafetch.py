#!/usr/bin/python
# -*- coding: utf-8 -*-

from instagram import client
from instagram.client import InstagramAPI

import requests
from models import Posts

import json
import logging
import time 
import ConfigParser
import codecs

logging.basicConfig(filename='fetcher.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

client_id = ''
Client_secret = ''
hashtag = ''
token = ''

class Fetcher:

    search_terms = []
    def __init__(self):
        
        Config = ConfigParser.ConfigParser()
        Config.readfp(codecs.open('config.ini', 'r', 'utf8'))
        
        self.token = Config.get('Instagram', 'token')
        self.search_terms = Config.get('Search_Terms', 'search_terms').split(',')


    def getJSON(self, term):
        endpoint = u'https://api.instagram.com/v1/tags/{0}/media/recent?access_token={1}'
        endpoint = endpoint.format(term, self.token)
        logging.info(endpoint)

        resp = requests.get(endpoint)

        if resp.status_code == 200:
            logging.info("yay, 200 response")
            return json.loads(resp.text)
        else:
            logging.warning("{0} - {1}".format(resp.status_code, resp.text))
            return None

            
    def saveMedia(self, term):
        media_json = self.getJSON(term)

        if not media_json:
            logging.info("Saved 0 media")
            return 0
            
        for media in media_json['data']:
            post = Posts()
            if not post.hasPost(int(media['id'].split('_')[0])):
                post.orig_post_id = int(media['id'].split('_')[0])
                post.orig_user_id = int(media['user']['id'])
                post.date = int(media['created_time'])
                post.username = media['user']['username']
                post.text = media['caption']['text']
                post.image_small = media['images']['low_resolution']['url']
                post.image_full = media['images']['standard_resolution']['url']
                post.service = 'instagram'
                post.likes = None
                post.orig_url = media['link']
                
                post.save()
            

if __name__ == "__main__":
    f = Fetcher()
    for term in f.search_terms:
        f.saveMedia(term)
