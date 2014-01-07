#!/usr/bin/env python

import urllib
import json
import getpass

class User:

    def __init__(self, username, portal=None, password=None):
        if portal == None:
            self.portalUrl = 'https://www.arcgis.com'
        else:
            self.portalUrl = portal
        self.username = username
        if password == None:
            self.password = getpass.getpass()
        else:
            self.password = password
        self.token = self.__getToken__(self.portalUrl, self.username, self.password)

    def __getToken__(self, url, username, password):
        '''Retrieves a token to be used with future requests.'''
        parameters = urllib.urlencode({'username' : username,
                                       'password' : password,
                                       'client' : 'referer',
                                       'referer': url,
                                       'expiration': 60,
                                       'f' : 'json'})
        response = urllib.urlopen(url + '/sharing/rest/generateToken?', parameters).read()
        token = json.loads(response)['token']
        return token

    def __portalId__(self):
        '''Gets the ID for the organization/portal.'''
        parameters = urllib.urlencode({'token' : self.token,
                                       'f' : 'json'})
        response = urllib.urlopen(self.portalUrl + '/sharing/rest/portals/self?' + parameters).read()
        portalId = json.loads(response)['id']
        return portalId
