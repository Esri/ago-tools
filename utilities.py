#!/usr/bin/env python

import urllib
import json

class Utilities:
    '''A class of tools for working with content in an AGO account'''
    def __init__(self, username, portal=None):
        from . import User
        self.user = User(username, portal)    

    def updateWebmapService(self, webmapId, oldUrl, newUrl):
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
                # Figure out which folder the item is in.
                itemFolder = self.__getItemFolder__(webmapId)
                #Post back the changes overwriting the old map
                modRequest = urllib.urlopen(self.user.portalUrl + '/sharing/content/users/' + self.user.username + '/' + itemFolder + '/addItem?' + params , urllib.urlencode(outParamObj))
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
            
    def updateItemUrl(self, itemId, oldUrl, newUrl):
        '''
        Use this to update the URL for items such as Map Images.
        The oldUrl parameter is required as a check to ensure you are not
        accidentally changing the wrong item or url.
        '''
        try:
            params = urllib.urlencode({'token' : self.user.token,
                                       'f' : 'json'})
            print 'Getting Info for: ' + itemId
            # Get the item data
            reqUrl = self.user.portalUrl + '/sharing/rest/content/items/' + itemId + '?' + params
            itemReq = urllib.urlopen(reqUrl).read()
            itemString = str(itemReq)
            
            # Double check that the existing URL matches the provided URL
            if itemString.find(oldUrl) > -1:
                # Figure out which folder the item is in.
                itemFolder = self.__getItemFolder__(itemId)
                # Update the item URL
                updateParams = urllib.urlencode({'url' : newUrl})
                updateUrl = self.user.portalUrl + '/sharing/rest/content/users/' + self.user.username + '/' + itemFolder + '/items/' + itemId + '/update?' + params
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
        parameters = urllib.urlencode({'token' : self.user.token,
                                       'f' : 'json'})
        response = json.loads(urllib.urlopen(self.user.portalUrl + '/sharing/rest/content/users/' + self.user.username + '?' + parameters).read())
        for item in response['items']:
            if item['id'] == itemId:
                return ''
            else:
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