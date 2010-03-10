#!/usr/bin/python
# -*- coding: utf-8 -*-

__auth__ = 'F0ur'
__version__ = '0.1'


import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/lib"))

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


if __name__ == '__main__':
    twitter = Twitter(Config.twitter_api)
    tweet_query = Tweet.all().order('-date')
    tweets = tweet_query.fetch(1)
    if len(tweets) == 0:
        message = twitter.getUserTimeline(Config.twitter_user, 1)
        if isinstance(message, list):
            tweet = Tweet()
            tweet.tid = str(message[0]["id"])
            tweet.put()
    else:
        messages = twitter.getUserTimeline(Config.twitter_user, since_id = tweets[0].tid, positive_seq = True)
        if isinstance(messages, list):
            for msg in messages:
                for service in Config.services.keys():
                    factory = serviceFactory()
                    s = factory.buildService(service.capitalize())
                    s.setCredentials(Config.services[service]["username"], Config.services[service]["password"])
                    s.postText(msg["text"])
                tweets[0].tid = str(msg["id"])
                tweets[0].put()
                time.sleep(Config.INTERVAL)
            #print "Send success"
        else:
            #print messages["message"]
            pass