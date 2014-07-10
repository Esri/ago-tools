#!/usr/bin/env python

import urllib
import json
import csv
import time

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

    def updateServiceItemsThumbnail(self, folder=None):
        '''
        Fetches catalog of items in portal. If there is no thumbnail, assigns the default.
        '''
        if(folder!=None):
            catalog = self.AGOLUserCatalog(folder,False)
        else:
            catalog=self.AGOLCatalog(None)

        for r in catalog:
            if(r.thumbnail==None):
                parameters = urllib.urlencode({'thumbnailURL' : 'http://static.arcgis.com/images/desktopapp.png', 'token' : self.user.token, 'f' : 'json'})

                requestToUpdate = self.user.portalUrl + '/sharing/rest/content/users/' + self.user.username  + '/items/' +r.id + '/update'

                try:
                    print ("updating " + r.title + " with thumbnail.")
                    response = urllib.urlopen(requestToUpdate, parameters ).read()

                    jresult = json.loads(response)
                except:
                    e=1

        return None

    def registerItems (self, mapservices, folder=''):
        '''
        Given a set of AGOL items, register them to the portal,
        optionally to a specific folder.
        '''
        self.servicesToRegister=mapservices

        if folder==None:
            folder=''

        icount=0
        i=0
        for ms in self.servicesToRegister.service_list:
            i = i +1

            sURL=ms.url
            sTitle=ms.title
            if ms.thumbnail==None:
                sThumbnail ='http://static.arcgis.com/images/desktopapp.png' 
            elif ms.id !=None:
                sThumbnail ="http://www.arcgis.com/sharing/content/items/" + ms.id + "/info/" + ms.thumbnail
            else:
                sThumbnail='http://static.arcgis.com/images/desktopapp.png' 

            #todo, handle map service exports

            sTags = 'mapping' if ms.tags==None else ms.tags
            sType= 'Map Service' if ms.type==None else ms.type
            sDescription = '' if ms.description==None else ms.description
            sSnippet = '' if ms.snippet ==None else ms.snippet
            sExtent = '' if ms.extent==None else ms.extent
            sSpatialReference='' if ms.spatialReference==None else ms.spatialReference
            sAccessInfo='' if ms.accessInformation==None else ms.accessInformation
            sLicenseInfo='' if ms.licenseInfo==None else ms.licenseInfo
            sCulture='' if ms.culture == None else ms.culture

            parameters = urllib.urlencode({'URL' : sURL,
                                           'title' : sTitle,
                                           'thumbnailURL' : sThumbnail,
                                           'tags' : sTags, 
                                           'description' : sDescription,
                                           'snippet': sSnippet,
                                           'extent':sExtent,
                                           'spatialReference':sSpatialReference,
                                           'accessInformation': sAccessInfo,
                                           'licenseInfo': sLicenseInfo,
                                           'culture': sCulture,
                                           'type' : sType,
                                           'token' : self.user.token,
                                           'f' : 'json'})
            #todo- use export map on map service items for thumbnail

            requestToAdd = self.user.portalUrl + '/sharing/rest/content/users/' + self.user.username + folder + '/addItem'

            try:
                if(sType.find('Service')>=0 or sType.find('Web Mapping Application')>=0):
                    response = urllib.urlopen(requestToAdd, parameters ).read()

                    jresult = json.loads(response)
                    print str(i) + ") " + ms.title + ": success= " + str(jresult["success"]) + "," + ms.url + ", " + "(" + jresult["id"] + ")"

                    if jresult["success"]:
                        icount=icount+1

            except:
                print str(i) + ") "  + ms.title + ':error!'

        print str(icount) + " item(s) added."

    def getFolderID(self, folderName):
        '''
        Return the ID of the folder with the given name.
        '''
        folders = self._getUserFolders()

        for f in folders:
            if str(f['title']) == folderName:
                return str(f['id'])

        return ''

    def _getUserFolders(self):
        '''
        Return all folder objects.
        '''
        requestToAdd = self.user.portalUrl + '/sharing/rest/content/users/' + self.user.username +  '?f=json&token=' + self.user.token;
        response = urllib.urlopen(requestToAdd).read()

        jresult = json.loads(response)        
        return jresult["folders"]

    def clearGroup(self, groupid):
        '''
        Unshare all content from the specified group.
        CAUTION
        '''
        groupcatalog = self.AGOLGroupCatalog(groupid)

        sItems=''
        for f in groupcatalog:
            requestToDelete = self.user.portalUrl + '/sharing/rest/content/items/' + f.id + "/unshare?groups=" + groupid

            parameters = urllib.urlencode({
                'token' : self.user.token,
                'f' : 'json'})
            print "Unsharing " + f.title

            response = urllib.urlopen(requestToDelete,parameters).read()

            jresult = json.loads(response)     

        print "Complete."
        return None

    def clearFolder(self, folderid):
        '''
        Delete all content from the specified folder.
        CAUTION
        '''
        foldercatalog = self.AGOLUserCatalog(folderid)
        sItems=''
        for f in foldercatalog:
            sItems+= f.id + ","

        if len(sItems)>0: sItems=sItems[:-1]

        requestToDelete = self.user.portalUrl + '/sharing/rest/content/users/' + self.user.username + "/deleteItems" 

        parameters = urllib.urlencode({'items':sItems,
                                       'token' : self.user.token,
                                       'f' : 'json'})

        print "Deleting " + str(len(foldercatalog)) + " items..."
        response = urllib.urlopen(requestToDelete,parameters).read()

        jresult = json.loads(response)     
        print "Complete."
        return None

    def AGOLGroupCatalog(self, groupid):
        '''
        Return the catalog of items in desiginated group.
        '''
        sCatalogURL=self.user.portalUrl + "/sharing/rest/search?q=%20group%3A" + groupid + "%20-type:%22Code%20Attachment%22%20-type:%22Featured%20Items%22%20-type:%22Symbol%20Set%22%20-type:%22Color%20Set%22%20-type:%22Windows%20Viewer%20Add%20In%22%20-type:%22Windows%20Viewer%20Configuration%22%20%20-type:%22Code%20Attachment%22%20-type:%22Featured%20Items%22%20-type:%22Symbol%20Set%22%20-type:%22Color%20Set%22%20-type:%22Windows%20Viewer%20Add%20In%22%20-type:%22Windows%20Viewer%20Configuration%22%20&num=100&sortField=title&sortOrder=asc"

        return self.AGOLCatalog(None,None,sCatalogURL)


    def AGOLUserCatalog(self, folder, includeSize=False):
        '''
        Return the catalog of CURRENT USER's items from portal, optionally from only a folder.
        '''
        sCatalogURL = self.user.portalUrl + "/sharing/rest/content/users/" + self.user.username + folder
        return self.AGOLCatalog(None,None,sCatalogURL)

    def AGOLCatalog(self, query=None, includeSize=False, sCatalogURL=None):
        '''
        Return all items from all users in a portal, optionally matching a 
        specified query.
        optionally make the additional requests for SIZE.
        sCatalogURL can be specified to use a specific folder
        '''

        resultCount = 0
        searchURL = ""
        viewURL = ""
        orgID = ""
        self.sFullSearch = ""
        self.bIncludeSize=includeSize

        self.orgID = self._getOrgID()

        self.catalogURL=sCatalogURL #for cataloging folders

        if self.user.portalUrl != None:
            self.searchURL = self.user.portalUrl  + "/sharing/rest" 
            self.viewURL = self.user.portalUrl  + "/home/item.html?id="

        self.query = query

        pList=[]
        allResults = []

        sQuery=self._getCatalogQuery(1,100)#get first batch

        print("fetching records 1-100...")

        response = urllib.urlopen(sQuery).read()
        jresult=json.loads(response)

        nextRecord = jresult['nextStart']
        totalRecords = jresult['total']
        num = jresult['num']
        start =jresult['start']

        #if this is a folder catalog, use items, not results
        sItemsProperty = 'results'
        if self.catalogURL!=None and str(self.catalogURL).find("/sharing/rest/content/users/")>0: sItemsProperty='items'

        pList = AGOLItems( jresult[sItemsProperty])

        for r in pList.AGOLItems_list:
            r.itemURL = self.viewURL + r.id
            r.created = time.strftime("%Y-%m-%d",time.gmtime(r.created/1000))
            r.modified = time.strftime("%Y-%m-%d",time.gmtime(r.modified/1000))
            if r.size== -1:
                r.size=0
            r.size = self._getSize(r)
            r.myRowID = len(allResults) + 1;
            allResults.append(r)

        if (nextRecord>0):
            while(nextRecord>0):
                sQuery = self._getCatalogQuery(nextRecord, 100)
                print("fetching records " + str(nextRecord) + "-" + str(nextRecord+100) + "...")

                response = urllib.urlopen(sQuery).read()
                jresult=json.loads(response)

                nextRecord = jresult['nextStart']
                totalRecords = jresult['total']
                num = jresult['num']
                start =jresult['start']

                pList = AGOLItems( jresult['results'])
                for r in pList.AGOLItems_list:
                    r.itemURL = self.viewURL + r.id
                    r.created = time.strftime("%Y-%m-%d",time.gmtime(r.created/1000))
                    r.modified = time.strftime("%Y-%m-%d",time.gmtime(r.modified/1000))
                    if r.size== -1:
                        r.size=0
                        r.size = self._getSize(r)
                    r.myRowID = len(allResults) + 1;

                    allResults.append(r)

        return allResults

    def _getSize(self, r):
        '''
        Issue query for item size.
        '''
        if(self.bIncludeSize != True):
            return 0

        print ("fetching size for " + r.title + " (" + r.type + ")")

        result=0
        sURL = self.searchURL + "/content/items/" + str(r.id) + "?f=json&token=" + self.user.token;

        response = urllib.urlopen(sURL).read()
        result = json.loads(response)['size']
        if(result>0):
            result = result/1024
        else:
            result=0

        return result

    def _getOrgID(self):
        '''
        Return the organization's ID.
        '''
        sURL = self.user.portalUrl + "/sharing/rest/portals/self?f=json&token=" + self.user.token

        response = urllib.urlopen(sURL).read()

        return str(json.loads(response)['id'])

    def _getCatalogQuery(self, start, num):
        '''
        Format a content query from specified start and number of records.
        '''
        sQuery=None
        if self.query != None:
            sQuery = self.query
        else:
            sQuery = self.sFullSearch

        if(self.catalogURL==None):
            sCatalogQuery = self.searchURL + "/search?q=" + sQuery
            if self.orgID != None:
                sCatalogQuery += " orgid:" + self.orgID
        else:
            #check to ensure ? vs &
            if(str(self.catalogURL).find('?')<0):
                char="?"
            else:
                char="&"

            sCatalogQuery = self.catalogURL + char + "ts=1" 

        sCatalogQuery += "&f=json&num="+ str(num) + "&start=" + str(start)
        sCatalogQuery += "&token=" + self.user.token

        return sCatalogQuery

    def updateUserRoles(self, users):
        self.usersToUpdate=users

        requestToUpdate= self.user.portalUrl + '/sharing/rest/portals/self/updateuserrole'

        for u in self.usersToUpdate.user_list:
            parameters = urllib.urlencode({'user':u.Username,
                                           'role':u.Role,
                                           'token' : self.user.token,
                                           'f' : 'json'})

            print "Updating Role for " + u.Username + " to " + u.Role + "..."
            response = urllib.urlopen(requestToUpdate,parameters).read()
            jresult = json.loads(response)     
            success= str(jresult["success"])
            print "Success: " + success

        print "Complete."
        return None

    
#collection of AGOLItem
class AGOLItems:
    def __init__ (self, item_list):
        self.AGOLItems_list=[]
        for item in item_list:
            self.AGOLItems_list.append(AGOLItem(item))

#AGOL item
class AGOLItem:
    def __init__(self, item_attributes):
        for k, v in item_attributes.items():
            setattr(self, k, v)

#collection of Map Services
class MapServices:
    def __init__ (self, import_list):
        self.service_list=[]
        for service in import_list:
            self.service_list.append(MapService(service))

#Map Service
class MapService:
    def __init__(self, service_attributes):
        for k, v in service_attributes.items():
            setattr(self, k, v)

#Collection of Usernames and roles
class UsersAttributes:
    def __init__ (self, import_list):
        self.user_list=[]
        for user in import_list:
            self.user_list.append(UserAttributes(user))

class UserAttributes:
    def __init__(self, user_attributes):
        for k, v in user_attributes.items():
            setattr(self, k, v)


