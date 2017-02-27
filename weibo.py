#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 17:00:31 2017

@author: will
"""
import urllib.request,urllib.parse

class APIClient(object):
    
#    app_key = '3755746530'
#    app_secret = '71f84726821585a0264d0fe8c8c71c11'
#    redirect_uri = 'http://127.0.0.1/'
    
    def __init__(self):
        app_key = '3755746530'
        app_secret = '71f84726821585a0264d0fe8c8c71c11'
        redirect_uri = 'http://127.0.0.1/'
        self.client_id = app_key
        self.client_secret = app_secret
        self.redirect_uri = redirect_uri
        
    def get_authorize_url(self):
        return 'https://api.weibo.com/oauth2/authorize?response_type=code&client_id=%s&redirect_uri=%s' %(self.client_id
                                                                                                          ,self.redirect_uri)
        
    def request_access_token(self):
        """post a request and then get a access_token"""
        para = {
                "client_id" : self.client_id,
                "client_secret" : self.client_secret,
                "redirect_uri" : self.redirect_uri,
                "code" : 'cc9d5805af0a3ac113f6cc14157c841f',
                "grant_type" : 'authorization_code'
                }
        data = urllib.parse.urlencode(para)
        data = data.encode(encoding='utf-8') 
        request = urllib.request.Request("https://api.weibo.com/oauth2/access_token",data=data)
        f = urllib.request.urlopen(request)
        return f.read()
