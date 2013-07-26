#!/usr/bin/env python

import urllib
import json
import csv

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
		
    def addNewUsersToGroups(self, daysToCheck, groups):
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

    def migrateAccount(self, userFrom, userTo):
        '''
        REQUIRES ADMIN ACCESS
        Transfers ownership of all items in userFrom's account to userTo's account, keeping same folder names.
        - Does not check for existing folders in userTo's account.
        - Does not delete content from userFrom's account.
        '''
        
		# request user content for userFrom
		# response contains list of items in root folder and list of all folders
        parameters = urllib.urlencode({'token': self.user.token, 'f': 'json'})
        request = self.user.portalUrl + '/sharing/rest/content/users/' + userFrom + '?' + parameters
        userContent = json.loads(urllib.urlopen(request).read())
		
		# create same folders in userTo's account like those in userFrom's account (requires POST)
        for folder in userContent['folders']:
            parameters2 = urllib.urlencode({'title' : folder['title'], 'token': self.user.token, 'f': 'json'})
            request2 = self.user.portalUrl + '/sharing/rest/content/users/' + userTo + '/createFolder?'           
            response2 = urllib.urlopen(request2, parameters2).read()

        # keep track of items and folders
        numberOfItems = 0
        numberOfFolders = 1
			
        # change ownership of items in ROOT folder (requires POST)
        for item in userContent['items']:
            parameters3 = urllib.urlencode({'targetUsername' : userTo, 'targetFoldername' : '/', 'token': self.user.token, 'f': 'json'})
            request3 = self.user.portalUrl + '/sharing/rest/content/users/' + userFrom + '/items/' + item['id'] + '/reassign?'
            response3 = urllib.urlopen(request3, parameters3).read()
            if 'success' in response3:
                numberOfItems += 1
		
        ### change ownership of items in SUBFOLDERS (nested loop)
        # request content in current folder
        for folder in userContent['folders']:
            parameters4 = urllib.urlencode({'token': self.user.token, 'f': 'json'})
            request4 = self.user.portalUrl + '/sharing/rest/content/users/' + userFrom + '/' + folder['id'] + '?' + parameters4
            folderContent = json.loads(urllib.urlopen(request4).read())
            numberOfFolders += 1

            # change ownership of items in CURRENT folder to userTo and put in correct folder (requires POST)
            for item in folderContent['items']:
                parameters5 = urllib.urlencode({'targetUsername' : userTo, 'targetFoldername' : folder['title'], 'token': self.user.token, 'f': 'pjson'})
                request5 = self.user.portalUrl + '/sharing/rest/content/users/' + userFrom + '/' + folder['id'] + '/items/' + item['id'] + '/reassign?'
                response5 = urllib.urlopen(request5, parameters5).read()
                numberOfItems += 1

        # summarize results
        print str(numberOfItems) + ' ITEMS in ' + str(numberOfFolders) + ' FOLDERS (incl. Home folder) copied'
        print '    from USER ' + userFrom + ' to USER ' + userTo
				
        return		

    def migrateAccounts(self, pathUserMappingCSV):
        '''
        REQUIRES ADMIN ACCESS
        Reassigns ownership of all content items between pairs of accounts specified in a CSV file.
        (i.e., this function batches migrateAccount using a CSV to feed in the accounts to migrate from/to)
        CSV should have two columns (no column headers/labels): col1=userFrom, col2=userTo
		'''

        with open(pathUserMappingCSV, 'rb') as userMappingCSV:
            userMapping = csv.reader(userMappingCSV)
            for user in userMapping:
                userFrom = user[0]
                userTo = user[1]
                print 'Copying items from ' + userFrom + ' to ' + userTo + '...'
                Admin.migrateAccount(self, userFrom, userTo)
                print

        return
