#### Delete items listed in an input CSV from  the organization
#### The only required fields in the CSV are:
#### id,owner 
#### Example:
#### deleteItems.py -u myuser -p mypassword -folder MyNewItems -portal https://esri.maps.arcgis.com -file c:\temp\agolinput.csv

import csv
import argparse
import sys

from agoTools.admin import Admin
from agoTools.admin import AGOLItems

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
parser.add_argument('-file', '--file')
parser.add_argument('-portal', '--portal')

args = parser.parse_args()
inputFile = ''

if args.file == None:
    args.file = _raw_input("CSV path: ")

if args.user == None:
    args.user = _raw_input("Username:")

if args.portal == None:
    args.portal = _raw_input("Portal: ")

args.portal = str(args.portal).replace("http://","https://")

agoAdmin = Admin(args.user,args.portal,args.password)

if args.file != None:
    inputFile=args.file

with open(inputFile) as input:
    dataReader = csv.DictReader(input)
    items=AGOLItems(dataReader)

agoAdmin.deleteItems(items.AGOLItems_list)
