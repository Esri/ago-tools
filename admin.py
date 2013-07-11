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
		
    def addUsersToGroups(self, daysToCheck, groups):
        '''
        REQUIRES ADMIN ACCESS
        Add new organization users to multiple groups and return a list of the status.
        '''
        # daysToCheck is the time interval to check for new users.
        # e.g. 1 will check past day, 7 will check past week, etc.
        # Provide one or more group IDs as strings (in quotes) separated by commas.
        # e.g. ['d93aabd856f8459a8905a5bd434d4d4a', 'f84c841a3dfc4591b1ff83281ea5025f']
        
        userSummary = []
        users = self.getUsers()
        
        # Create a list of all new users (joined in the last 'daysToCheck' days).
        newUsers = []
        for user in users:
            if date.fromtimestamp(float(user['created'])/1000) > date.today()-timedelta(days=daysToCheck):
                newUsers.append(user)
        
        # Assign new users to the specified group(s).
        parameters = urllib.urlencode({'token': self.user.token, 'f': 'json'})
        for groupID in groups:
            for newUser in newUsers:
                userSummary.append(newUser)
                user = newUser['username']
                print 'Attempting to add ' + user + ' to groupID ' + groupID
                # Add Users - REQUIRES POST method (undocumented operation as of 2013-07-10).
                response = urllib.urlopen(self.user.portalUrl + '/sharing/rest/community/groups/' + groupID + '/addUsers?', 'users=' + user + "&" + parameters).read()
                print response +' NOTE: May return "notAdded" even if successful.  Confirm addition on ArcGIS.com.'
                print ''
                
        return userSummary

