#!/usr/bin/python
# -*- coding: utf-8 -*-

__auth__ = 'F0ur'
__version__ = '0.1'

import urllib
import urllib2
import base64
import time
import urlparse

from django.utils import simplejson

class Api(object):
    '''A python interface into the Microblog API'''
    
    _API_REALM = ''
    _API_URL = {}
    _SOURCE = 'Tw2other-p'
    
    def __init__(self,
                 username = None,
                 password = None,
                 input_encoding = None,
                 request_headers = None,
                 ):
        '''Instantiate a new Api object.
        
        Args:
          username: The username of the microblog account.  [optional]
          password: The password for the microblog account. [optional]
          input_encoding: The encoding used to encode input strings. [optional]
          request_header: A dictionary of additional HTTP request headers. [optional]
        '''
        self._urllib = urllib2
        self._input_encoding = input_encoding

        self._initRequestHeaders(request_headers)
        self._initUserAgent()
        self._initDefaultParameters()
        self.setCredentials(username, password)
    
    def postText(self, text):
        '''Post a  pure text status message from the authenticated user.
        
        Args:
          text:
            The message text to be posted.
        '''
        if not self._username:
            return None
        self.setSource()
        data = {self._API_URL["update"]["fieldName"] : text}
        url = self._API_URL["base"]["url"] + self._API_URL["update"]["url"]
        json = self._fetchUrl(url, post_data = data)
        data = simplejson.loads(json)
        return data
        
    def getUserTimeline(self,
                         user = None,
                         count = None,
                         since = None, 
                         since_id = None,
                         positive_seq = False):
        '''Fetch the sequence of public messages for a single user.
            The Api instance must be authenticated if the user is private.
    
            Args:
              user:
                either the username (short_name) or id of the user to retrieve.  If
                not specified, then the current authenticated user is used. [optional]
              count: the number of status messages to retrieve [optional]
              since:
                Narrows the returned results to just those statuses created
                after the specified HTTP-formatted date. [optional]
              since_id:
                Returns only public statuses with an ID greater than (that is,
                more recent than) the specified ID. [Optional]
        '''
        if user:
          url = self._API_URL["base"]["url"] + self._API_URL["user_timeline"]["url"] + '?id=%s' % user
        elif not user and not self.username:
          pass
        else:
          url = self._API_URL["base"]["url"] + self._API_URL["user_timeline"]["url"] + '?id=%s' % self.username
        parameters = {}
        if count is not None:
          parameters['count'] = count
        if since:
          parameters['since'] = since
        if since_id:
          parameters['since_id'] = since_id
        json = self._fetchUrl(url, parameters = parameters)
        if not positive_seq:
            return simplejson.loads(json)
        else:
            data = simplejson.loads(json)
            if isinstance(data, list):
                data.sort(cmp = lambda x, y : cmp(x["id"], y["id"]))
            return data
    
    def setCredentials(self, username, password):
        '''Set the username and password for this instance
        
        Args:
          username: The microblog username.
          password: The microblog password.
        '''
        self._username = username
        self._password = password
    
    def clearCredentials(self):
        '''Clear the username and password for this instance'''
        self._username = None
        self._password = None
    
    def setUrllib(self, urllib):
        '''Override the default urllib implementation.
        
        Args:
          urllib: an instance that supports the same API as the urllib2 module
        '''
        self._urllib = urllib
    
    def setUserAgent(self, user_agent):
        '''Override the default user agent
        
        Args:
          user_agent: a string that should be send to the server as the User-agent
        '''
        self._request_headers['User-Agent'] = user_agent
    
    
    def setSource(self):
        '''Suggest the "from source" value to be displayed on the microblog web site.
        
        The value of the 'source' parameter must be first recognized by
        the microblog server.  New source values are authorized on a case by
        case basis by the microblog development team.
        
        Args:
          source:
            The source name as a string.  Will be sent to the server as
            the 'source' parameter.
        '''
        self._default_params['source'] = self._SOURCE
    
    def _buildUrl(self, url, path_elements = None, extra_params = None):
        # Break url into consituent parts
        (scheme, netloc, path, params, query, fragment) = urlparse.urlparse(url)
    
        # Add any additional path elements to the path
        if path_elements:
            # Filter out the path elements that have a value of None
            p = [i for i in path_elements if i]
            if not path.endswith('/'):
                path += '/'
            path += '/'.join(p)
    
        # Add any additional query parameters to the query string
        if extra_params and len(extra_params) > 0:
            extra_query = self._encodeParameters(extra_params)
            # Add it to the existing query
            if query:
                query += '&' + extra_query
            else:
                query = extra_query
    
        # Return the rebuilt URL
        return urlparse.urlunparse((scheme, netloc, path, params, query, fragment))
    
    def _initRequestHeaders(self, request_headers):
        if request_headers:
            self._request_headers = request_headers
        else:
            self._request_headers = {}
    
    def _initUserAgent(self):
        user_agent = 'Python-urllib/%s (tw2other-gae-python/%s)' % \
                     (self._urllib.__version__, __version__)
        self.setUserAgent(user_agent)
    
    def _initDefaultParameters(self):
        self._default_params = {}
    
    def _addAuthorizationHeader(self, username, password):
        if username and password:
            basic_auth = base64.encodestring('%s:%s' % (username, password))[:-1]
            self._request_headers['Authorization'] = 'Basic %s' % basic_auth
    
    def _removeAuthorizationHeader(self):
        if self._request_headers and 'Authorization' in self._request_headers:
            del self._request_headers['Authorization']
    
    def _getOpener(self, url, username = None, password = None):
        if username and password:
            self._addAuthorizationHeader(username, password)
            handler = self._urllib.HTTPBasicAuthHandler()
            (scheme, netloc, path, params, query, fragment) = urlparse.urlparse(url)
            handler.add_password(Api._API_REALM, netloc, username, password)
            opener = self._urllib.build_opener(handler)
        else:
            opener = self._urllib.build_opener()
        opener.addheaders = self._request_headers.items()
        return opener
    
    def _encode(self, s):
        if self._input_encoding:
            return unicode(s, self._input_encoding).encode('utf-8')
        else:
            return unicode(s).encode('utf-8')
 
    def _encodeParameters(self, parameters):
        '''Return a string in key=value&key=value form
        
        Values of None are not included in the output string.
        
        Args:
          parameters:
            A dict of (key, value) tuples, where value is encoded as
            specified by self._encoding
        Returns:
          A URL-encoded string in "key=value&key=value" form
        '''
        if parameters is None:
            return None
        else:
            return urllib.urlencode(dict([(k, self._encode(v)) for k, v in parameters.items() if v is not None]))
    
    def _encodePostData(self, post_data):
        '''Return a string in key=value&key=value form
        
        Values are assumed to be encoded in the format specified by self._encoding,
        and are subsequently URL encoded.
        
        Args:
          post_data:
            A dict of (key, value) tuples, where value is encoded as
            specified by self._encoding
        Returns:
          A URL-encoded string in "key=value&key=value" form
        '''
        if post_data is None:
            return None
        else:
            return urllib.urlencode(dict([(k, self._encode(v)) for k, v in post_data.items()]))
    
    def _fetchUrl(self,
                  url,
                  post_data = None,
                  parameters = None):
        '''Fetch a URL, optionally caching for a specified time.
        
        Args:
          url: The URL to retrieve
          post_data: 
            A dict of (str, unicode) key/value pairs.  If set, POST will be used.
          parameters:
            A dict whose key/value pairs should encoded and added 
            to the query string. [OPTIONAL]
          no_cache: If true, overrides the cache on the current request
        
        Returns:
          A string containing the body of the response.
        '''
        try:
            # Build the extra parameters dict
            extra_params = {}
            if self._default_params:
                extra_params.update(self._default_params)
            if parameters:
                extra_params.update(parameters)
            
            # Add key/value parameters to the query string of the url
            url = self._buildUrl(url, extra_params = extra_params)
            # Get a url opener that can handle basic auth
            opener = self._getOpener(url, username = self._username, password = self._password)
            
            encoded_post_data = self._encodePostData(post_data)
            
            # Open and return the URL immediately if we're not going to cache
            url_data = opener.open(url, encoded_post_data).read()
            opener.close()
            
        except urllib2.HTTPError, ex:
            if ex.code == 200: message = '200 OK: 一切正常' 
            elif ex.code == 304: message = '304 Not Modified: 没有任何新数据.'
            elif ex.code == 400: message = '400 Bad Request: 不合法的请求.'
            elif ex.code == 401: message = '401 Not Authorized: 没有进行用户验证.'
            elif ex.code == 403: message = '403 Forbidden: 请求被禁止访问的信息.'
            elif ex.code == 404: message = '404 Not Found: 没有指定的记录.'
            elif ex.code == 500: message = '500 Internal Server Error: API内部错误.'
            elif ex.code == 502: message = '502 Bad Gateway: API服务当掉或正在升级.'
            elif ex.code == 503: message = '503 Service Unavailable: API服务负载过重，稍后再试.'
            else: message = 'Unkown HTTPError: 未知网络错误'
            ret_dict = {'error': True, 
                        'message': message }
            return simplejson.dumps(ret_dict, sort_keys = True)
 
        # Always return the latest version
        return url_data