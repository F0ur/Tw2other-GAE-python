#!/usr/bin/python
# -*- coding: utf-8 -*-

__auth__ = 'F0ur'
__version__ = '0.1'



class Config():
    """Common config for tw2other-gae-python"""
    
    INTERVAL = 10
    
    twitter_sync_level = 1
    
    twitter_api = 'http://twitter.com/'
    
    twitter_user = 'your_twitter_id'
    
    services = {
                "Renjian" : {"username" : "your_username", "password" : "your_password"}            
                }
