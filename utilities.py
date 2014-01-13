#!/usr/bin/env python

import urllib
import json

def searchPortal(portal, query=None, totalResults=None, sortField='numviews', sortOrder='desc', token=None):
    '''
    Search the portal using the specified query and search parameters.
    Optionally provide a token to return results visible to that user.
    More examples on advanced search operators here:
    https://github.com/esri/ago-tools/blob/master/search-cheat-sheet.md
    '''
    # Default results are returned by highest number of views in descending order.
    allResults = []
    if not totalResults or totalResults > 100:
        numResults = 100
    else:
        numResults = totalResults
    results = __search__(portal, query, numResults, sortField, sortOrder, 0, token)

    if not 'error' in results.keys():
        if not totalResults:
            totalResults = results['total'] # Return all of the results.
        allResults.extend(results['results'])
        while results['nextStart'] > 0 and results['nextStart'] < totalResults:
            # Do some math to ensure it only returns the total results requested.
            numResults = min(totalResults - results['nextStart'] + 1, 100)
            results = __search__(portal=portal, query=query, numResults=numResults, sortField=sortField,
                                sortOrder=sortOrder, token=token, start=results['nextStart'])
            allResults.extend(results['results'])
        return allResults
    else:
        print results['error']['message']
        return results

def __search__(portal, query=None, numResults=100, sortField='numviews', sortOrder='desc', start=0, token=None):
    '''Retrieve a single page of search results.'''
    params = {
        'q': query,
        'num': numResults,
        'sortField': sortField,
        'sortOrder': sortOrder,
        'f': 'json',
        'start': start
    }
    if token:
        params['token'] = token # Adding a token provides an authenticated search.
    request = portal + '/sharing/rest/search?' + urllib.urlencode(params)
    results = json.loads(urllib.urlopen(request).read())
    return results

class Utilities:
    '''A class of tools for working with content in an AGO account'''
    def __init__(self, username, portal=None, password=None):
        from . import User
        self.user = User(username, portal, password)

    def updateWebmapService(self, webmapId, oldUrl, newUrl, folderID=None):
        try:
            params = urllib.urlencode({'token' : self.user.token,
                                       'f' : 'json'})
            print 'Getting Info for: ' + webmapId
            #Get the item data
            reqUrl = self.user.portalUrl + '/sharing/content/items/' + webmapId + '/data?' + params
            itemDataReq = urllib.urlopen(reqUrl).read()
            itemString = str(itemDataReq)

            #See if it needs to be updated
            if itemString.find(oldUrl) > -1:
                #Update the map
                newString = itemString.replace(oldUrl, newUrl)
                #Get the item's info for the addItem parameters
                itemInfoReq = urllib.urlopen(self.user.portalUrl + '/sharing/content/items/' + webmapId + '?' + params)
                itemInfo = json.loads(itemInfoReq.read(), object_hook=self.__decode_dict__)
                print 'Updating ' + itemInfo['title']

                #Set up the addItem parameters
                outParamObj = {
                    'extent' : ', '.join([str(itemInfo['extent'][0][0]), str(itemInfo['extent'][0][1]), str(itemInfo['extent'][1][0]), str(itemInfo['extent'][1][1])]),
                    'type' : itemInfo['type'],
                    'item' : itemInfo['item'],
                    'title' : itemInfo['title'],
                    'overwrite' : 'true',
                    'tags' : ','.join(itemInfo['tags']),
                    'text' : newString
                }
                # Get the item folder.
                if itemInfo['ownerFolder']:
                    folderID = itemInfo['ownerFolder']
                else:
                    folderID = ''
                #Post back the changes overwriting the old map
                modRequest = urllib.urlopen(self.user.portalUrl + '/sharing/content/users/' + self.user.username + '/' + folderID + '/addItem?' + params , urllib.urlencode(outParamObj))
                #Evaluate the results to make sure it happened
                modResponse = json.loads(modRequest.read())
                if modResponse.has_key('error'):
                    raise AGOPostError(webmapId, modResponse['error']['message'])
                else:
                    print "Successfully updated the urls"
            else:
                print 'Didn\'t find any services for ' + oldUrl
        except ValueError as e:
            print 'Error - no web maps specified'
        except AGOPostError as e:
            print 'Error updating web map ' + e.webmap + ": " + e.msg

    def updateItemUrl(self, itemId, oldUrl, newUrl, folderID=None):
        '''
        Use this to update the URL for items such as Map Services.
        The oldUrl parameter is required as a check to ensure you are not
        accidentally changing the wrong item or url.
        This can also replace part of a URL. The text of oldUrl is replaced with the text of newUrl. For example you could change just the host name of your URLs.
        '''
        try:
            params = urllib.urlencode({'token' : self.user.token,
                                       'f' : 'json'})
            print 'Getting Info for: ' + itemId
            # Get the item data
            reqUrl = self.user.portalUrl + '/sharing/rest/content/items/' + itemId + '?' + params
            itemReq = urllib.urlopen(reqUrl).read()
            itemString = str(itemReq)
            itemInfo = json.loads(itemString)

            if not itemInfo.has_key('url'):
                print itemInfo['title'] + ' doesn\'t have a url property'
                return
            print 'Updating ' + itemInfo['title']
            existingURL = itemInfo['url']

            # Double check that the existing URL matches the provided URL
            if itemString.find(oldUrl) > -1:
                # Get the item folder.
                if itemInfo['ownerFolder']:
                    folderID = itemInfo['ownerFolder']
                else:
                    folderID = ''
                # Update the item URL
                updatedURL = existingURL.replace(oldUrl, newUrl)
                updateParams = urllib.urlencode({'url' : updatedURL})
                updateUrl = self.user.portalUrl + '/sharing/rest/content/users/' + self.user.username + '/' + folderID + '/items/' + itemId + '/update?' + params
                updateReq = urllib.urlopen(updateUrl, updateParams).read()
                modResponse = json.loads(updateReq)
                if modResponse.has_key('success'):
                    print "Successfully updated the url."
                else:
                    raise AGOPostError(itemId, modResponse['error']['message'])
            else:
                print 'Didn\'t find the specified old URL: ' + oldUrl
        except ValueError as e:
            print e
        except AGOPostError as e:
            print 'Error updating item: ' + e.msg

    def updatewebmapversionAGX(self, webmapId, folderID=None):
        '''Update the web map version from 1.9x to 1.7x so that the new web maps can be opened in ArcGIS Explorer Online.'''
        try:
            params = urllib.urlencode({'token' : self.user.token,
                                       'f' : 'json'})
            print 'Getting Info for: ' + webmapId
            #Get the item data
            reqUrl = self.user.portalUrl + '/sharing/content/items/' + webmapId + '/data?' + params
            itemDataReq = urllib.urlopen(reqUrl).read()
            itemString = str(itemDataReq)

            itemString = itemString.replace('1.9', '1.7')

            itemInfoReq = urllib.urlopen(self.user.portalUrl + '/sharing/content/items/' + webmapId + '?' + params)
            itemInfo = json.loads(itemInfoReq.read(), object_hook=self.__decode_dict__)
            print 'Updating ' + itemInfo['title']

            #Set up the addItem parameters
            outParamObj = {
                'extent' : ', '.join([str(itemInfo['extent'][0][0]), str(itemInfo['extent'][0][1]), str(itemInfo['extent'][1][0]), str(itemInfo['extent'][1][1])]),
                'type' : itemInfo['type'],
                'item' : itemInfo['item'],
                'title' : itemInfo['title'],
                'overwrite' : 'true',
                'tags' : ','.join(itemInfo['tags']),
                'text' : itemString
            }
            # Get the item folder.
            if itemInfo['ownerFolder']:
                folderID = itemInfo['ownerFolder']
            else:
                folderID = ''

            #Post back the changes overwriting the old map
            modRequest = urllib.urlopen(self.user.portalUrl + '/sharing/content/users/' + self.user.username + '/' + folderID + '/addItem?' + params , urllib.urlencode(outParamObj))
            #Evaluate the results to make sure it happened
            modResponse = json.loads(modRequest.read())
            if modResponse.has_key('error'):
                raise AGOPostError(webmapId, modResponse['error']['message'])
            else:
                print "Successfully updated the version"

        except ValueError as e:
            print 'Error - no web maps specified'
        except AGOPostError as e:
            print 'Error updating web map ' + e.webmap + ": " + e.msg

    def getFolderItems(self, folderId, userName=None):
        '''
        Returns all items (list of dictionaries) for an AGOL folder using the folder ID.
        folderID -- The unique id for the folder. Use getFolderID to find the folder ID for a folder name.
        userName -- The user who owns the folder. If not specified, the user initialized with this object is used.
        '''
        if userName == None:
            userName = self.user.username
        params = urllib.urlencode({'token': self.user.token, 'f': 'json'})
        request = self.user.portalUrl + '/sharing/rest/content/users/' + userName + '/' + folderId + '?' + params
        folderContent = json.loads(urllib.urlopen(request).read())
        return folderContent['items']

    def getUserFolders(self, userName=None):
        '''
        Returns all folders (list of dictionaries) for an AGOL user.
        userName -- The user who owns the folder. If not specified, the user initialized with this object is used.
        '''
        if userName == None:
            userName = self.user.username
        parameters = urllib.urlencode({'token': self.user.token, 'f': 'json'})
        request = self.user.portalUrl + '/sharing/rest/content/users/' + userName + '?' + parameters
        userContent = json.loads(urllib.urlopen(request).read())
        return userContent['folders']

    def getFolderID(self, folderTitle, userName=None):
        '''
        Returns the folder ID given a case insensitive folder title.
        folderTitle -- The title (name) of a folder.
        userName -- The user who owns the folder. If not specified, the user initialized with this object is used.
        '''
        if userName == None:
            userName = self.user.username
        folders = self.getUserFolders(userName)
        for folder in folders:
            if folder['title'].upper() == folderTitle.upper():
                return folder['id']
                break

    def updateURLs(self, oldUrl, newUrl, items, folderID=None):
        '''
        Updates the URL or URL part for all URLs in a list of AGOL items.
        This works for all item types that store a URL. (e.g. web maps, map services, applications, etc.)
        oldUrl -- All or part of a URL to search for.
        newUrl -- The text that will be used to replace the current "oldUrl" text.
        '''
        for item in items:
            if item['type'] == 'Web Map':
                self.updateWebmapService(item['id'], oldUrl, newUrl, folderID)
            else:
                if item.has_key('url') and not item['url'] == None:
                    self.updateItemUrl(item['id'], oldUrl, newUrl, folderID)

    def __decode_dict__(self, dct):
        newdict = {}
        for k, v in dct.iteritems():
            k = self.__safeValue__(k)
            v = self.__safeValue__(v)
            newdict[k] = v
        return newdict

    def __safeValue__(self, inVal):
        outVal = inVal
        if isinstance(inVal, unicode):
            outVal = inVal.encode('utf-8')
        elif isinstance(inVal, list):
            outVal = self.__decode_list__(inVal)
        return outVal

    def __decode_list__(self, lst):
        newList = []
        for i in lst:
            i = self.__safeValue__(i)
            newList.append(i)
        return newList

    def __getItemFolder__(self, itemId):
        '''Finds the foldername for a particular item.'''
        # This method is probably not needed anymore as the item folder
        # is returned in the description response ('ownerFolder').
        # Recommend deprecating this function or rewriting it to use the simple
        # description request and return 'ownerFolder'.
        parameters = urllib.urlencode({'token' : self.user.token,
                                       'f' : 'json'})
        response = json.loads(urllib.urlopen(self.user.portalUrl + '/sharing/rest/content/users/' + self.user.username + '?' + parameters).read())
        for item in response['items']:
            if item['id'] == itemId:
                return ''
        for folder in response['folders']:
            folderContent = self.__getFolderContent__(folder['id'])
            for item in folderContent['items']:
                if item['id'] == itemId:
                    return folder['id']

    def __getFolderContent__(self, folderId):
        '''Lists all of the items in a folder.'''
        parameters = urllib.urlencode({'token' : self.user.token,
                                       'f' : 'json'})
        response = json.loads(urllib.urlopen(self.user.portalUrl + '/sharing/rest/content/users/' + self.user.username + '/' + folderId + '?' + parameters).read())
        return response

class AGOPostError(Exception):
    def __init__(self, webmap, msg):
        self.webmap = webmap
        self.msg = msg
