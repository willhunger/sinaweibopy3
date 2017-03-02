#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 17:00:31 2017

@author: will
"""
import urllib.request
import urllib.parse
import json
import logging
import time


def _obj_hook(paris):
    'json encode'
    odict = JsonDict()
    for key, value in paris.items():
        odict[str(key)] = value
    return odict

def _encode_params(**kw):
    'Encode parameters'
    args = []
    for key, value in kw.items():
        para = value.encode('utf-8') if isinstance(value, str) else str(value)
        args.append('%s=%s' % (key, urllib.parse.quote(para)))
    return '&'.join(args)


class JsonDict(dict):
    '''
    a json class inhert dict class which can use d['key'] or d.key to get
    '''
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

_HTTP_GET = 0
_HTTP_POST = 1
_HTTP_UPLOAD = 2

def _http_get(url, authorization=None, **kw):
    logging.info('GET %s' % url)
    return _http_request(url, _HTTP_GET, authorization, **kw)

def _http_post(url, authorization=None, **kw):
    logging.info('POST %s' % url)
    return _http_request(url, _HTTP_POST, authorization, **kw)

def _http_upload(url, authorization=None, **kw):
    logging.info('UPLOAD %s' % url)
    return _http_request(url, _HTTP_UPLOAD, authorization, **kw)

def _http_request(url, method, authorization, **kw):
    'send http request and get json object'
    params = None
    boundary = None
    if method == _HTTP_UPLOAD:
        pass
    else:
        params = _encode_params(**kw)
    http_url = '%s?%s' % (url, params) if method == _HTTP_GET else url
    http_para = None if method == _HTTP_GET else params.encode(encoding='utf-8')
    req = urllib.request.Request(http_url, data=http_para)
    if authorization:
        pass
    if boundary:
        pass
    resq = urllib.request.urlopen(req)
    body = resq.read().decode("utf-8")
    result = json.loads(body, object_hook=_obj_hook)
    if 'error_code' in result:
        print('error')
    return result



class APIClient(object):
    'APIClient class'
    def __init__(self, app_key, app_secret, redirect_uri=None,
                 response_type='code', domain='api.weibo.com', version='2'):
        self.client_id = app_key
        self.client_secret = app_secret
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.auth_url = 'https://%s/oauth2/' % domain
        self.api_url = 'https://%s/%s/' % (domain, version)
        self.access_token = None
        self.expires = 0.0

    def get_authorize_url(self):
        'get authorize url'
        return '''https://api.weibo.com/oauth2/authorize?response_type=\
code&client_id=%s&redirect_uri=%s'''%(self.client_id, self.redirect_uri)


    def request_access_token(self, code):
        """post a request and then get a access_token"""
        result = _http_post('%s%s' % (self.auth_url, 'access_token'), \
                          client_id=self.client_id, \
                          client_secret=self.client_secret, \
                          redirect_uri=self.redirect_uri, \
                          code=code, grant_type='authorization_code')
        result.expires_in += int(time.time())
        return result


    def set_access_token(self, access_token, expires_in):
        'set access_token and expires_in'
        self.access_token = str(access_token)
        self.expires = float(expires_in)

    def public_timeline(self):
        '''
        get new public weibo,the parameters followed can be used in _http_get in this method
        access_token : (string) the token you got after OAuth
        count : (int) the record items in one single page,default 50 items
        page : (int) the page number,default one page
        base_app : (int) whether get data in current app or not,
            0 is not(all data),1 is yes(current app),default 0
        '''
        result = _http_get('%s'% (self.api_url)  + 'statuses/public_timeline.json', \
                           access_token=self.access_token, \
                           count=50, \
                           page=1, \
                           base_app=0, \
                )
        return result


def main():
    '''
    if you want to use this api,you should follow steps follows to operate.
    '''
    try:
        #step 1 : sign a app in weibo and then define const app key,app srcret,redirect_url
        APP_KEY = '3755746530'
        APP_SECRET = '71f84726821585a0264d0fe8c8c71c11'
        REDIRECT_URL = 'http://127.0.0.1/'
        #step 2 : get authorize url and code
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=REDIRECT_URL)
        print(client.get_authorize_url())
        #step 3 : get Access Token
        result = client.request_access_token(input("please input code : "))
        client.set_access_token(result.access_token, result.expires_in)
        #step 4 : using api by access_token
        print(client.public_timeline())
    except ValueError:
        print('pyOauth2Error')

if __name__ == '__main__':
    main()
