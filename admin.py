#!/usr/bin/env python

import urllib
import json

class Admin:
    '''A class of tools for administering AGO Orgs or Portals'''
    def __init__(self, username, portal=None):
        from . import User
        self.user = User(username, portal)
    
    def __users__(self, start=0):
        '''Retrieve a single page of users.'''
        parameters = urllib.urlencode({'token' : self.user.token,
                                       'f' : 'json',
                                       'start' : start,
                                       'num' : 100})
        portalId = self.user.__portalId__()
        response = urllib.urlopen(self.user.portalUrl + '/sharing/rest/portals/' + portalId + '/users?' + parameters).read()
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
