#!/usr/bin/python
# -*- coding: utf-8 -*-

__auth__ = 'F0ur'
__version__ = '0.1'

import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from api import *

class Renjian(Api):
    ''' A python interface into the Renjian API
    
        Example usage:
    
        To create an instance of the renjian.Renjian class, with no authentication:
    
          >>> import renjian
          >>> renjian = renjian.Renjian()
        
        To use authentication, instantiate Api class with a
        username and password:

          >>> renjian = renjian.Renjian('renjian username', 'renjian password')
    
    
        To post a renjian status message (after being authenticated):
    
          >>> message = renjian.postText('Hello World!')
          
        To get some renjian status messages (without being authenticated):
    
          >>> messages = renjian.getUserTimeline('id or short_name')  
    '''
    
    _API_REALM = 'Renjian API'
    _API_URL = {
                    "base" : {"url" : "http://api.renjian.com/"},
                    "update" : {"url" : "statuses/update.json", "fieldName" : "text"}
                 }
    
    def __init__(self, username = None, password = None):
        Api.__init__(self, username, password)

        
