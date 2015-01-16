import arcpy
import json
import argparse
import sys
import json
import urllib
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


#parameters
##########


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user')
parser.add_argument('-p', '--password')
parser.add_argument('-portal', '--portal')
parser.add_argument('-itemid', '--itemid')
parser.add_argument('-webmap', '--webmap')
parser.add_argument('-mxd','--mxd')
parser.add_argument('-groupLayer','--groupLayer')
parser.add_argument('-poiLayerName','--poiLayerName')
parser.add_argument('-aoiLayerName','--aoiLayerName')
parser.add_argument('-descriptionField','--descriptionField')

args = parser.parse_args()

if args.user == None:
    args.user = _raw_input("Username:")

if args.portal == None:
    args.portal = _raw_input("Portal: ")

args.portal = str(args.portal).replace("http://","https://")

agoAdmin = Admin(args.user,args.portal,args.password)

if args.itemid == None:
    args.itemid = _raw_input("Application Item Id: ")

if args.webmap == None:
    args.webmap = _raw_input("webMap Id: ")

if args.mxd == None:
    args.mxd= _raw_input("Map Document Path: ")

if args.groupLayer == None:
    args.groupLayer= _raw_input("Group Layer Name: ")

if args.poiLayerName == None:
    args.poiLayerName= _raw_input("POI Layer Name: ")

if args.aoiLayerName == None:
    args.aoiLayerName= _raw_input("AOI Layer Name: ")

if args.descriptionField == None:
    args.descriptionField= _raw_input("Description Field Name: ")

webmapid=args.webmap#'2105a270e16548eabff5f94e07110034'
mxd =args.mxd# r"D:\data\RevolutionaryWar\WarMapsV4.mxd"
#sFileOut = r"D:\atemp\finalDataOut.json"
#sDataFile="d:/atemp/inputdata5.json"

groupLayerName =args.groupLayer# 'Battles'
poiLayerName =args.poiLayerName# "Battlesite"
aoiLayerName = args.aoiLayerName#"Troop Movements"
descriptionField=args.descriptionField#"DESCRIPTION"
appItemId=args.itemid
#outFile = r"D:\atemp\sectionsOut2.json"
##########

sJSON='"sections": ['
sJSON='['

layers = arcpy.mapping.ListLayers(arcpy.mapping.MapDocument(mxd))

#for each layer in the map:
for layer in layers:

  #find our target group layer of sections:
  if layer.isGroupLayer and layer.name == groupLayerName: 
    
    print "Found Section Group Layer: " + groupLayerName + "."
    for subLayer in layer:

      #if this sub layer is a group layer it is a section:
      if subLayer.isGroupLayer:

        sectionGroupLayer = subLayer        
        section=sectionGroupLayer.name
        print "Reading '" + section + "'..."

        for subLayer2 in sectionGroupLayer:
          if subLayer2.name == poiLayerName:
            poiLayer=subLayer2
             
            #open first record
            with arcpy.da.SearchCursor(poiLayer.dataSource,descriptionField,poiLayer.definitionQuery) as cursor:
              for row in cursor:
                sectionDescription = row[0]
                sectionDescription = sectionDescription.replace(r'"',r'\"')

          if subLayer2.name == aoiLayerName:
            aoiLayer=subLayer2
            sectionExtent=aoiLayer.getExtent(True)

        try:
          section=sectionGroupLayer.name
        except:
          section=sectionGroupLayer.name

        try:
          sExtentJSON = sectionExtent.JSON
        except:
          sExtentJSON="{}"

        sJSON+='{'
        sJSON+=r'"title":' + r'"<strong><span style=\"font-size: 36px\">' + str(section) + r'</span></strong>"'
        sJSON+=','
    
        sJSON += r'"content":"'
        sJSON = sJSON + sectionDescription
        sJSON += r'"'

        sJSON+=','
        sJSON+='"contentActions": [],'
        sJSON+= r'"status": "PUBLISHED",'
        sJSON+='"media": {"type": "webmap","webmap": {"id": "' + webmapid + '","extent": ' + sExtentJSON + ',"layers": null,"popup": null,"overview": {"enable": true,"openByDefault": true},"legend": {"enable": false,"openByDefault": false}}'
        
        sJSON+='}},'

#trim last ","
sJSON=sJSON.rstrip(',')
sJSON+=']'

#print sJSON

#f = open(outFile, 'w')
sOut=sJSON.encode("utf-8","replace")

print "generated sections JSON"
#f.write(sOut)

##############
#handle inserting into datafile

sJSONIn = sOut
sJSONIn2=unicode(sJSONIn,"cp866").encode("utf-8")
#sJSONIn2="{" + sJSONIn2 + "}"
my_sections=json.loads(sJSONIn2)


#sContent = open(sDataFile, 'rb').read()
#get from data request

parameters = urllib.urlencode({'token': agoAdmin.user.token, 'f': 'json'})
request = agoAdmin.user.portalUrl + '/sharing/rest/content/items/' + args.itemid +'/data?' + parameters
#sContent = json.loads(urllib.urlopen(request).read())

#sContent2=unicode(sContent,"cp866").encode("utf-8")

itemDataReq = urllib.urlopen(request).read()
my_data = json.loads(itemDataReq, object_hook=agoAdmin.__decode_dict__)

#my_data = json.loads(sContent2)

#print my_data

#s=json.loads('{"sections":[]}')

my_data['values']['story']['sections'] =my_sections

pJSON=my_data#['values']['story']['sections']

#sFileOut=r'd:/atemp/test.txt' #SBTEST
#f = open (sFileOut,"w")
#s2=s2.encode("utf-8","replace")

sJSON=json.dumps(pJSON)
sJSON=sJSON.encode("utf-8","replace")
#f.write(sJSON)

#post
outParamObj = {
    'text' : sJSON
}

parameters = urllib.urlencode({'token': agoAdmin.user.token, 'f': 'json'})
requestUpdate = agoAdmin.user.portalUrl + '/sharing/rest/content/users/' + args.user + '/items/' + args.itemid +'/update?' + parameters
sResult= json.loads(urllib.urlopen(requestUpdate,urllib.urlencode(outParamObj)).read())



print "complete.  Success: " + str(sResult["success"])


