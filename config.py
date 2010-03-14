#!/usr/bin/python
# -*- coding: utf-8 -*-

__auth__ = 'F0ur'
__version__ = '0.1'



class Config():
    """Common config for tw2other-gae-python"""
    #每条消息间隔时间，单位为秒，不建议修改
    INTERVAL = 10
    #简单的消息过滤等级
    #0为不过滤
    #1为过滤回复消息
    #2为过滤RT消息
    #3为过滤回复消息和RT消息
    twitter_sync_level = 1
    #Twitter API地址，一般不用修改
    twitter_api = 'http://twitter.com/'
    #Twitter User Name,可以是id或者short_name
    twitter_user = 'twitter_id or twitter_short_name'
    #同步地点选择，如果不需要，用#号注释
    services = {
                "Renjian" : {"username" : "renjian_username", "password" : "renjian_password"},
                "Digu" : {"username" : "digu_username", "password" : "digu_password"},
                #"Other" : {"username" : "other_username", "password" : "other_password"},
                }
