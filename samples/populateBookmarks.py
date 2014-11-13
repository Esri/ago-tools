#### Update a webmap with a collection of bookmarks
#### Input json file format:
####
####
####
#{"bookmarks": [
#{
#  "extent":{
#    "SpatialReference":{
#      "wkid":"4326"
#    },
#    "xmax":-77.58890542503474,
#    "xmin":-77.66083839947551,
#    "ymax":42.58041413631198,
#    "ymin":42.549020481314585
#  },
#  "name":"Area of Interest 1"
#},
#{
#  "extent":{
#    "SpatialReference":{
#      "wkid":"4326"
#    },
#    "xmax":-77.53970779419222,
#    "xmin":-77.59446878554364,
#    "ymax":42.57963402941389,
#    "ymin":42.51842215653264
#  },
#  "name":"Area of Intest 2"
#}
#}
#### examples:
#### populateBookmarks.py -u <username> -p <password> -jsonfile c:/temp/matownsbookmarks.json -labelfield NAME -itemid ff2251d13c094cbc857ae0787900355b -portal http://yourorg.maps.arcgis.com
#### populateBookmarks.py -u <username> -p <password>  -layerURL http://services.arcgis.com/XWaQZrOGjgrsZ6Cu/arcgis/rest/services/Towns/FeatureServer/0 -labelfield NAME -itemid ff2251d13c094cbc857ae0787900355b -portal http://<org>.maps.arcgis.com
#### populateBookmarks.py -u <username> -p <password>  -fc D:/data/SteubenCounty/Data.gdb/Districts -labelfield NAME -itemid ff2251d13c094cbc857ae0787900355b -portal http://<org>.maps.arcgis.com

import csv
import argparse
import sys
import json
from agoTools.admin import Admin

def _raw_input(prompt=None, stream=None, input=None):
    # A raw_input() replacement that doesn't save the string in the
    # GNU readline history.
    if not stream:
        stream = sys.stderr
    if not input:
        input = sys.stdin
    prompt = str(prompt)
    if prompt:
        stream.write(prompt)
        stream.flush()
    # NOTE: The Python C API calls flockfile() (and unlock) during readline.
    line = input.readline()
    if not line:
        raise EOFError
    if line[-1] == '\n':
        line = line[:-1]
    return line

# return value with quotes around it always
def getResultValueWithQuotes(s):
    if (s==None):
        return ''
    try:
        sResult = str(s)
        if (sResult.find("\"")>0):
            sResult = sResult.replace("\"","\"\"")
        return "\"" + str(sResult) + "\""

    except:
        return ''

# return value with quotes if needed
def getResultValue(s):
    if (s==None):
        return ''
    try:
        sResult = str(s)
        if(sResult.find(",")>0 or sResult.find("\r\n")>0):
            sResult = sResult.replace("\"", "\"\"")
            return "\"" + str(sResult) + "\""
        else:
            return str(sResult)
    except:
        return ''

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user')
parser.add_argument('-p', '--password')
parser.add_argument('-itemid', '--itemid')
parser.add_argument('-layerID', '--layerID')
parser.add_argument('-fcID', '--fcID')
parser.add_argument('-layerURL', '--layerURL')
parser.add_argument('-labelfield', '--labelfield')
parser.add_argument('-jsonfile', '--jsonfile')
parser.add_argument('-portal', '--portal')
parser.add_argument('-fc','--fc')

args = parser.parse_args()

if args.user == None:
    args.user = _raw_input("Username:")

if args.portal == None:
    args.portal = _raw_input("Portal: ")

args.portal = str(args.portal).replace("http://","https://")

agoAdmin = Admin(args.user,args.portal,args.password)

if args.itemid == None:
    args.itemid = _raw_input("WebMap Id: ")

if args.labelfield == None:
    args.labelfield="NAME"

if args.layerID!=None:
    args.layerURL=agoAdmin.getLayerURL(args.layerID)

if args.layerURL!= None:
    pBookmarks =agoAdmin.createBookmarksFromLayer(args.layerURL,args.labelfield)
elif args.fc !=None:
    pBookmarks = agoAdmin.readBookmarksFromFeatureClass(args.fc,args.labelfield)
elif args.jsonfile != None:
    pBookmarks= agoAdmin.readBookmarksFromFile(args.jsonfile)
elif args.fcID !=None:
    pBookmarks = agoAdmin.readBookmarksFromFeatureCollection(args.fcID,args.labelfield)
else:
    args.jsonfile = _raw_input("json file: ")
    pBookmarks= agoAdmin.readBookmarksFromFile(args.jsonfile,args.labelfield)

#sBookmarks=json.JSONEncoder().encode(pBookmarks);
if pBookmarks!=None:
    agoAdmin.addBookmarksToWebMap(pBookmarks,args.itemid);
else:
    print "No Bookmarks were found."
