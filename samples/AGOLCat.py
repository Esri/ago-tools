import csv
import argparse
import sys

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
parser.add_argument('-q', '--query')
parser.add_argument('-file', '--file')
parser.add_argument('-portal', '--portal')
parser.add_argument('-size', '--bIncludeSize')

args = parser.parse_args()

if args.file == None:
  args.file = _raw_input("CSV path: ")

if args.user == None:
  args.user = _raw_input("Username:")

if args.portal == None:
  args.portal = _raw_input("Portal: ")
 
args.portal = str(args.portal).replace("http://","https://")

bIncludeSize=False
if(args.bIncludeSize == "True"):
  bIncludeSize=True

agoAdmin = Admin(args.user,args.portal,args.password)

catalog= agoAdmin.AGOLCatalog(args.query,bIncludeSize)

with open(args.file, 'wb') as output:
    # Write header row.
    output.write("id,owner,created,modified,name, itle,type,typeKeywords,description,tags,snippet,thumbnail,extent,spatialReference,accessInformation,licenseInfo,culture,url,access,size,listed,numComments,numRatings,avgRatings,numViews,itemURL\n")
    # Write item data.
    for r in catalog:
      s=''
      s += getResultValue(r.id) + ","
      s += getResultValue(r.owner) + ","
      s += getResultValue(r.created) + ","
      s += getResultValue(r.modified) + ","
      s += getResultValue(r.name) + ","
      s += getResultValue(r.title) + ","
      s += getResultValue(r.type) + ","

      sKeyWords = ""
      for sKW in r.typeKeywords:
        sKeyWords += sKW + ","

      if (len(sKeyWords)> 0 and sKeyWords.endswith(",")):
        sKeyWords = sKeyWords[:-1]
      
      s += getResultValue(sKeyWords) + ","
      s += getResultValue(r.description) + ","

      sTags = ""
      for sKW in r.tags:
        sTags += sKW + ","
      
      if (len(sTags)> 0 and sTags.endswith(",")):
        sTags = sTags[:-1]

      s += getResultValue(sTags) + ","
      s += getResultValue(r.snippet) + ","
      s += getResultValue(r.thumbnail) + ","
      s += "" + ","

      s += getResultValue(r.spatialReference) + ","
      s += getResultValue(r.accessInformation) + ","
      s += getResultValue(r.licenseInfo) + ","
      s += getResultValue(r.culture) + ","

      s += getResultValue(r.url) + ","
      s += getResultValue(r.access) + ","
      s += getResultValue(r.size) + ","

      s += getResultValue(r.listed) + ","
      s += getResultValue(r.numComments) + ","
      s += getResultValue(r.numRatings) + ","
      s += getResultValue(r.avgRating) + ","
      s += getResultValue(r.numViews) + ","


      s += getResultValue(r.itemURL);
      s+="\n"

      output.writelines(s)

    print (args.file + " written.")
    a=1

