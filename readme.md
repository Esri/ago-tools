agolTools
=========

A Python package to assist with administering ArcGIS Online Organizations.

#### Installation
Unzip into a folder such as C:/myscripts, then either:

* add that directory to your system path in advanced system settings
* append it at runtime using the sys module in python
    
    `import sys`
    
    `sys.path.append('c:/myscripts')`

    
## Sample usage

### Admin Class
 
#### Create a spreadsheet of all users in the org
	import csv
    from agolTools.admin import Admin
    agolAdmin = Admin(<username>)
    users = agolAdmin.getUsers()

    outputDir = 'c:/temp'
    outputFile = outputDir + '/users.csv'

    with open(outputFile, 'wb') as outputFile:
        dataWriter = csv.writer(outputFile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # Write header row.
        dataWriter.writerow(['Full Name', 'Username', 'Role'])
        #Write user data.
        for user in users:
            dataWriter.writerow([user['fullName'], user['username'], user['role']])

            
### Utilities Class
            
#### Update map service urls in webmaps
    from agolTools.utilities import Utilities
    myAgolUtilities = Utilities(<username>)

    webmapId = 'e1d78110b0eg447aab46d373c7360046'
    oldUrl = 'http://myserver.com/arcgis/rest/services/old/MapServer'
    newUrl = 'http://myserver.com/arcgis/rest/services/new/MapServer'

    myAgolUtilities.updateWebmapService(webmapId, oldUrl, newUrl)