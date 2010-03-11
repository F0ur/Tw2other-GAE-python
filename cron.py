#!/usr/bin/python
# -*- coding: utf-8 -*-

__auth__ = 'F0ur'
__version__ = '0.1'


import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/lib"))

import re
from renjian import *
from twitter import *
from config import *
from google.appengine.ext import db

class serviceFactory():
    def buildService(self, service):
        if service == "Renjian":
            return Renjian()
        return None
    
class Tweet(db.Model):
    tid = db.StringProperty(multiline = False)
    date = db.DateTimeProperty(auto_now_add = True)

class Filter():
    @staticmethod
    def match(tweet, sync_level):
        if re.match(Pattern.getPattern(sync_level), tweet):
            if sync_level == 0:
                return False
            return True
        return False
    
class Pattern():
    @staticmethod
    def getPattern(sync_level):
        if sync_level == 0:
            return ''
        elif sync_level == 1:
            return '@.*'
        elif sync_level == 2:
            return 'RT\s@.*'
        elif sync_level == 3:
            return 'RT\s|@'
        else:
            return ''


if __name__ == '__main__':
    twitter = Twitter(Config.twitter_api)
    tweetid_query = Tweet.all().order('-date')
    tweetid = tweetid_query.fetch(1)
    if len(tweetid) == 0:
        tweet = twitter.getUserTimeline(Config.twitter_user, 1)
        if isinstance(message, list):
            tweetid = Tweet()
            tweetid.tid = str(tweet[0]["id"])
            tweetid.put()
    else:
        tweets = twitter.getUserTimeline(Config.twitter_user, since_id = tweetid[0].tid, positive_seq = True)
        if isinstance(tweets, list):
            for tweet in tweets:
                if Filter.match(tweet["text"], Config.twitter_sync_level):
                    continue
                for service in Config.services.keys():
                    factory = serviceFactory()
                    s = factory.buildService(service.capitalize())
                    s.setCredentials(Config.services[service]["username"], Config.services[service]["password"])
                    s.postText(tweet["text"])
                tweetid[0].tid = str(tweet["id"])
                tweetid[0].put()
                time.sleep(Config.INTERVAL)
            #print "Send success"
        else:
            #print messages["message"]
            pass