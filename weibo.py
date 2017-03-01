#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 17:00:31 2017

@author: will
"""
import urllib.request,urllib.parse
import json,logging,time


def _obj_hook(paris):
    'json encode'
    o = JsonDict()
    for k, v in paris.items():
        o[str(k)] = v
    return o
    


class JsonDict(dict):
    '''
    a json class inhert dict class which can use d['key'] or d.key to get
    '''
    def __getattr__(self, attr):
        return self[attr]
    
    def __setattr__(self, attr, value):
        self[attr] = value
            

class APIClient(object):
    'APIClient class'
    def __init__(self, app_key, app_secret, redirect_uri):
        self.client_id = app_key
        self.client_secret = app_secret
        self.redirect_uri = redirect_uri
        
    def get_authorize_url(self):
        'get authorize url'
        return 'https://api.weibo.com/oauth2/authorize?response_type=code&client_id=%s&redirect_uri=%s' %(self.client_id
                                                                                                          ,self.redirect_uri)
        
    def request_access_token(self,code):
        """post a request and then get a access_token"""
        para = {
                "client_id" : self.client_id,
                "client_secret" : self.client_secret,
                "redirect_uri" : self.redirect_uri,
                "code" : code,
                "grant_type" : 'authorization_code'
                }
        data = urllib.parse.urlencode(para)
        data = data.encode(encoding='utf-8') 
        request = urllib.request.Request("https://api.weibo.com/oauth2/access_token",data=data)
        res = urllib.request.urlopen(request)
        resq = res.read().decode("utf-8")
        r = json.loads(resq, object_hook=_obj_hook)
        logging.info(r)
        r.expires_in += int(time.time())
        return r
    
    def set_access_token(self,access_token, expires_in):
        self.access_token = str(access_token)
        self.expires = float(expires_in)
        
        
    
    def main():
        try:
            # step 1 : sign a app in weibo and then define const app key,app srcret,redirect_url
            APP_KEY = "3755746530"
            APP_SECRET = "71f84726821585a0264d0fe8c8c71c11"
            REDIRECT_URL = 'http://127.0.0.1/'
            # step 2 : get authorize url and code
            client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=REDIRECT_URL)
            print(client.get_authorize_url())
            # step 3 : get Access Token
            r = client.request_access_token(input("please input code"))
            client.set_access_token(r.access_token, r.expires_in)
            # step 4 : using api bu access_token 
        except Exception as pyOauth2Error:
            print(pyOauth2Error)
            
    if __name__ == '__main__':
        main()