#!/usr/bin/python
# -*- coding: utf-8 -*-

__auth__ = 'F0ur'
__version__ = '0.1'

import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from api import *

class Twitter(Api):
    ''' A python interface into the Twitter API
    
        Example usage:
    
        To create an instance of the renjian.Renjian class, with no authentication:
    
          >>> import twitter
          >>> twitter = twitter.Twitter()
        
        To use authentication, instantiate the twitter.Api class with a
        username and password:

          >>> twitter = twitter.Twitter('renjian username', 'renjian password')
    
    
        To post a twitter status message (after being authenticated):
    
          >>> message = twitter.postText('Hello World!')
          
        To get some twitter status messages (without being authenticated):
    
          >>> messages = twitter.getUserTimeline('id or short_name')  
    '''
    
    _API_REALM = 'Twitter API'
    _API_URL = {
                    "base" : {"url" : ""},
                    "user_timeline" : {"url" : "statuses/user_timeline.json"}
                 }
    
    def __init__(self, api_url, username = None, password = None):
        Api.__init__(self, username, password)
        if not api_url.endswith('/'):
            api_url += '/'
        self._API_URL["base"]["url"] = api_url
    