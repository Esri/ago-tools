#!/usr/bin/env python

import urllib
import json
import getpass

class admin:
    
    def __init__(self, username, portal=None):
        if portal == None:
            self.portalUrl = 'https://arcgis.com'
        self.username = username
        self.password = getpass.getpass()        
        self.token = self.__getToken__(self.portalUrl, self.username, self.password)

    def __getToken__(self, url, username, password):
        '''Retrieves a token to be used with future requests.'''
        parameters = urllib.urlencode({'username' : username,
                                       'password' : password,
                                       'client' : 'requestip',
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
    
    def __users__(self, start=0):
        '''Retrieve a single page of users.'''
        parameters = urllib.urlencode({'token' : self.token,
                                       'f' : 'json',
                                       'start' : start,
                                       'num' : 100})
        portalId = self.__portalId__()
        response = urllib.urlopen(self.portalUrl + '/sharing/rest/portals/' + portalId + '/users?' + parameters).read()
        users = json.loads(response)
        return users    
    
    def getUsers(self):
        ''' Returns a list of all users in the organization (requires admin access).'''
        allUsers = []
        users = self.__users__()
        for user in users['users']:
            allUsers.append(user)
        while users['nextStart'] > 0:
            users = self.__users__(users['nextStart'])
            for user in users['users']:
                allUsers.append(user)       
        return allUsers
