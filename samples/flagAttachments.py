#### calculate a field for feature layer indicating presence of attachments

#### example:
#### flagAttachment.py -u <username> -p <password> -flagField HASATTACHMENTS -layerURL http://services.arcgis.com/XWaQZrOGjgrsZ6Cu/arcgis/rest/services/Towns/FeatureServer/0  -portal http://yourorg.maps.arcgis.com

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

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user')
parser.add_argument('-p', '--password')
parser.add_argument('-layerURL', '--layerURL')
parser.add_argument('-layerID', '--layerID')
parser.add_argument('-flagField', '--flagField')
parser.add_argument('-portal', '--portal')

args = parser.parse_args()

if args.user == None:
    args.user = _raw_input("Username:")

if args.portal == None:
    args.portal = _raw_input("Portal: ")

args.portal = str(args.portal).replace("http://","https://")

agoAdmin = Admin(args.user,args.portal,args.password)

if args.flagField == None:
    args.flagField="HASATTACHMENTS"

if (args.layerID==None and args.layerURL==None):
    args.layerID = _raw_input("layerID: ")

if args.layerID!=None:
    args.layerURL=agoAdmin.getLayerURL(args.layerID)

agoAdmin.calculateAttachmentCount(args.layerURL,args.flagField)

