#!/usr/bin/python
# -*- coding: utf-8 -*-

__auth__ = 'F0ur'
__version__ = '0.1'

import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from api import *

class Digu(Api):
    ''' A python interface into the Digu API
    
        Example usage:
    
        To create an instance of the digu.digu class, with no authentication:
    
          >>> import digu
          >>> digu = digu.Digu()
        
        To use authentication, instantiate Api class with a
        username and password:

          >>> digu = digu.Digu('digu username', 'digu password')
    
    
        To post a digu status message (after being authenticated):
    
          >>> message = digu.postText('Hello World!')
          
        To get some digu status messages (without being authenticated):
    
          >>> messages = digu.getUserTimeline('id or short_name')  
    '''
    
    _API_REALM = 'Digu API'
    _API_URL = {
                    "base" : {"url" : "http://api.minicloud.com.cn/"},
                    "update" : {"url" : "statuses/update.json", "fieldName" : "content"}
                 }
    
    def __init__(self, username = None, password = None):
        Api.__init__(self, username, password)

        
