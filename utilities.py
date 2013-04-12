#!/usr/bin/env python

import urllib
import json

class Utilities:
    def updateMapService(self, webmap, oldUrl, newUrl):
        try:
            params = urllib.urlencode({'token' : self.token,
                                       'f' : 'json'})
            print 'Getting Info for: ' + webmap
            #Get the item data
            reqUrl = self.portalUrl + '/sharing/content/items/' + webmap + '/data?' + params
            print reqUrl
            itemDataReq = urllib.urlopen(reqUrl).read()
            itemString = str(itemDataReq)
            print itemString
            print itemString.find(oldUrl)
            #See if it needs to be updated
            if itemString.find(oldUrl) > -1:
                print 'found it...updating now'
                #Update the map
                newString = itemString.replace(oldUrl, newUrl)
                #Get the item's info for the addItem parameters
                itemInfoReq = urllib.urlopen(self.portalUrl + '/sharing/content/items/' + webmap + '?' + params)
                itemInfo = json.loads(itemInfoReq.read(), object_hook = self.__decode_dict__)
                print '------------------'
                print '2) ' + str(itemInfo)
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
                print '--------------------'
                print '3) ' + urllib.urlencode(outParamObj)
                # Figure out which folder the item is in
                itemFolder = self.__getItemFolder__(webmap)
                #Post back the changes overwriting the old map
                modRequest = urllib2.urlopen(self.portalUrl + '/sharing/content/users/' + self.username + '/' + itemFolder + '/addItem?' + params , urllib.urlencode(outParamObj))
                #Evaluate the results to make sure it happened
                modResponse = json.loads(modRequest.read())
                print modResponse
                if modResponse.has_key('error'):
                    raise AGOPostError(webmap, modResponse['error']['message'])
        except ValueError as e:
            print 'Error - no web maps specified'
        except AGOPostError as e:
            print 'Error updating web map ' + e.webmap + ": " + e.msg        
                
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
        parameters = urllib.urlencode({'token' : self.token,
                                       'f' : 'json'})
        response = json.loads(urllib.urlopen(self.portalUrl + '/sharing/rest/content/users/' + self.username + '?' + parameters).read())
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
        parameters = urllib.urlencode({'token' : self.token,
                                       'f' : 'json'})
        response = json.loads(urllib.urlopen(self.portalUrl + '/sharing/rest/content/users/' + self.username + '/' + folderId + '?' + parameters).read())
        return response
        
class AGOPostError(Exception):
    def __init__(self, webmap, msg):
        self.webmap = webmap
        self.msg = msg    