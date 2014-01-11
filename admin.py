#!/usr/bin/env python

import urllib
import json
import csv
from datetime import date, timedelta

class Admin:
    '''A class of tools for administering AGO Orgs or Portals'''
    def __init__(self, username, portal=None, password=None):
        from . import User
        self.user = User(username, portal, password)

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

    def getUsers(self, roles=None, daysToCheck=10000):
        '''
        Returns a list of all users in the organization (requires admin access).
        Optionally provide a list of roles to filter the results (e.g. ['org_publisher']).
        Optionally provide a number to include only accounts created in the last x number of days.
        '''
        if not roles:
            roles = ['org_admin', 'org_publisher', 'org_user']
            #roles = ['org_admin', 'org_publisher', 'org_author', 'org_viewer'] # new roles to support Dec 2013 update
        allUsers = []
        users = self.__users__()
        for user in users['users']:
            if user['role'] in roles and date.fromtimestamp(float(user['created'])/1000) > date.today()-timedelta(days=daysToCheck):
                allUsers.append(user)
        while users['nextStart'] > 0:
            users = self.__users__(users['nextStart'])
            for user in users['users']:
                if user['role'] in roles and date.fromtimestamp(float(user['created'])/1000) > date.today()-timedelta(days=daysToCheck):
                    allUsers.append(user)
        return allUsers

    def addUsersToGroups(self, users, groups):
            '''
            REQUIRES ADMIN ACCESS
            Add organization users to multiple groups and return a list of the status
            '''
            # Provide one or more usernames in a list.
            # e.g. ['user_1', 'user_2']
            # Provide one or more group IDs in a list.
            # e.g. ['d93aabd856f8459a8905a5bd434d4d4a', 'f84c841a3dfc4591b1ff83281ea5025f']

            toolSummary = []

            # Assign users to the specified group(s).
            parameters = urllib.urlencode({'token': self.user.token, 'f': 'json'})
            for group in groups:
                # Add Users - REQUIRES POST method (undocumented operation as of 2013-11-12).
                response = urllib.urlopen(self.user.portalUrl + '/sharing/rest/community/groups/' + group + '/addUsers?', 'users=' + ','.join(users) + "&" + parameters).read()
                # Users not added will be reported back with each group.
                toolSummary.append({group: json.loads(response)})

            return toolSummary

    def reassignAllUser1ItemsToUser2(self, userFrom, userTo):
        '''
        REQUIRES ADMIN ACCESS
        Transfers ownership of all items in userFrom/User1's account to userTo/User2's account, keeping same folder names.
        - Does not check for existing folders in userTo's account.
        - Does not delete content from userFrom's account.
        '''

        # request user content for userFrom
        # response contains list of items in root folder and list of all folders
        parameters = urllib.urlencode({'token': self.user.token, 'f': 'json'})
        request = self.user.portalUrl + '/sharing/rest/content/users/' + userFrom + '?' + parameters
        userContent = json.loads(urllib.urlopen(request).read())

        # create same folders in userTo's account like those in userFrom's account
        for folder in userContent['folders']:
            parameters2 = urllib.urlencode({'title' : folder['title'], 'token': self.user.token, 'f': 'json'})
            request2 = self.user.portalUrl + '/sharing/rest/content/users/' + userTo + '/createFolder?'
            response2 = urllib.urlopen(request2, parameters2).read()   # requires POST

        # keep track of items and folders
        numberOfItems = 0
        numberOfFolders = 1

        # change ownership of items in ROOT folder
        for item in userContent['items']:
            parameters3 = urllib.urlencode({'targetUsername' : userTo, 'targetFoldername' : '/', 'token': self.user.token, 'f': 'json'})
            request3 = self.user.portalUrl + '/sharing/rest/content/users/' + userFrom + '/items/' + item['id'] + '/reassign?'
            response3 = urllib.urlopen(request3, parameters3).read()   # requires POST
            if 'success' in response3:
                numberOfItems += 1

        ### change ownership of items in SUBFOLDERS (nested loop)
        # request content in current folder
        for folder in userContent['folders']:
            parameters4 = urllib.urlencode({'token': self.user.token, 'f': 'json'})
            request4 = self.user.portalUrl + '/sharing/rest/content/users/' + userFrom + '/' + folder['id'] + '?' + parameters4
            folderContent = json.loads(urllib.urlopen(request4).read())
            numberOfFolders += 1

            # change ownership of items in CURRENT folder to userTo and put in correct folder
            for item in folderContent['items']:
                parameters5 = urllib.urlencode({'targetUsername' : userTo, 'targetFoldername' : folder['title'], 'token': self.user.token, 'f': 'pjson'})
                request5 = self.user.portalUrl + '/sharing/rest/content/users/' + userFrom + '/' + folder['id'] + '/items/' + item['id'] + '/reassign?'
                response5 = urllib.urlopen(request5, parameters5).read()   # requires POST
                numberOfItems += 1

        # summarize results
        print '    ' + str(numberOfItems) + ' ITEMS in ' + str(numberOfFolders) + ' FOLDERS (incl. Home folder) copied'
        print '        from USER ' + userFrom + ' to USER ' + userTo

        return

    def reassignAllGroupOwnership(self, userFrom, userTo):
        '''
        REQUIRES ADMIN ACCESS
        Reassigns ownership of all groups between a pair of accounts.
        '''
        groups = 0
        groupsReassigned = 0

        # Get list of userFrom's groups
        print 'Requesting ' + userFrom + "'s group info from ArcGIS Online...",
        parameters = urllib.urlencode({'token': self.user.token, 'f': 'pjson'})
        request = self.user.portalUrl + '/sharing/rest/community/users/' + userFrom + '?' + parameters
        response = urllib.urlopen(request).read()
        userFromContent = json.loads(response)
        print 'RECEIVED!'

        # Determine if userFrom is group owner and, if so, transfer ownership to userTo
        print 'Checking groups...',
        for group in userFromContent['groups']:
            print '.',
            groups += 1
            if group['owner'] == userFrom:
                parameters = urllib.urlencode({'targetUsername' : userTo, 'token': self.user.token, 'f': 'pjson'})
                request = self.user.portalUrl + '/sharing/rest/community/groups/' + group['id'] + '/reassign?'
                response = urllib.urlopen(request, parameters).read()   # requires POST
                if 'success' in response:
                    groupsReassigned += 1

        # Report results
        print
        print '    CHECKED ' + str(groups) + ' groups ASSOCIATED with ' + userFrom + '.'
        print '       REASSIGNED ' + str(groupsReassigned) + ' groups OWNED by ' + userFrom + ' to ' + userTo + '.'

        return

    def addUser2ToAllUser1Groups(self, userFrom, userTo):
        '''
        REQUIRES ADMIN ACCESS
        Adds userTo/User2 to all groups that userFrom/User1 is a member
        '''

        groups = 0
        groupsOwned = 0
        groupsAdded = 0

        # Get list of userFrom's groups
        parameters = urllib.urlencode({'token': self.user.token, 'f': 'pjson'})
        request = self.user.portalUrl + '/sharing/rest/community/users/' + userFrom + '?' + parameters
        response = urllib.urlopen(request).read()
        userFromContent = json.loads(response)

        # Add userTo to each group that userFrom's is a member, but not an owner
        for group in userFromContent['groups']:
            groups += 1
            if group['owner'] == userFrom:
                groupsOwned += 1
            else:
                parameters = urllib.urlencode({'users' : userTo, 'token': self.user.token, 'f': 'pjson'})
                request = self.user.portalUrl + '/sharing/rest/community/groups/' + group['id'] + '/addUsers?'
                response = urllib.urlopen(request, parameters).read()   # requires POST
                if '[]' in response:   # This currently undocumented operation does not correctly return "success"
                    groupsAdded += 1

        print '    CHECKED ' + str(groups) + ' groups associated with ' + userFrom + ':'
        print '        ' + userFrom +  ' OWNS ' + str(groupsOwned) + ' groups (' + userTo + ' NOT added).'
        print '        ' + userTo + ' is already a MEMBER of ' + str(groups-groupsOwned-groupsAdded) + ' groups.'
        print '        ' + userTo + ' was ADDED to ' + str(groupsAdded) + ' groups.'

        return

    def migrateAccount(self, userFrom, userTo):
        '''
        REQUIRES ADMIN ACCESS
        Reassigns ownership of all content items and groups from userFrom to userTo.
        Also adds userTo to all groups which userFrom is a member.
        '''

        print 'Copying all items from ' + userFrom + ' to ' + userTo + '...'
        self.reassignAllUser1ItemsToUser2(self, userFrom, userTo)
        print

        print 'Reassigning groups owned by ' + userFrom + ' to ' + userTo + '...'
        self.reassignAllGroupOwnership(self, userFrom, userTo)
        print

        print 'Adding ' + userTo + ' as a member of ' + userFrom + "'s groups..."
        self.addUser2ToAllUser1Groups(self, userFrom, userTo)
        return

    def migrateAccounts(self, pathUserMappingCSV):
        '''
        REQUIRES ADMIN ACCESS
        Reassigns ownership of all content items and groups between pairs of accounts specified in a CSV file.
        Also adds userTo to all groups which userFrom is a member.
        This function batches migrateAccount using a CSV to feed in the accounts to migrate from/to,
        the CSV should have two columns (no column headers/labels): col1=userFrom, col2=userTo)
        '''

        with open(pathUserMappingCSV, 'rb') as userMappingCSV:
            userMapping = csv.reader(userMappingCSV)
            for user in userMapping:
                userFrom = user[0]
                userTo = user[1]

                print '=========='
                print 'Copying all items from ' + userFrom + ' to ' + userTo + '...'
                self.reassignAllUser1ItemsToUser2(self, userFrom, userTo)
                print

                print 'Reassigning groups owned by ' + userFrom + ' to ' + userTo + '...'
                self.reassignAllGroupOwnership(self, userFrom, userTo)
                print

                print 'Adding ' + userTo + ' as a member of ' + userFrom + "'s groups..."
                self.addUser2ToAllUser1Groups(self, userFrom, userTo)
                print '=========='
        return