# ago-tools

A Python package to assist with administering ArcGIS Online Organizations.

## Features
* Create a spreadsheet of all users in the org
* Update map service urls in webmaps
* Search for new users and add them to a list of groups
* Move (migrate) all items between accounts (single or batch)

## Instructions

1. Fork and then clone the repo. 
2. Run and try the samples.

## Installation
Unzip into a folder such as C:/myscripts and remove dashes from the directory name.
e.g. `C:/myscripts/ago-tools-master` to `C:/myscripts/agoTools`

Then do one of the following:

* add that directory to your system path in advanced system settings
* append it at runtime using the sys module in python
    
        import sys
        sys.path.append('c:/myscripts')

## Samples

#### Admin Class
 
#### Create a spreadsheet of all users in the org
    # Requires admin role.
    import csv, time
    from agoTools.admin import Admin
	
    agoAdmin = Admin(<username>) # Replace <username> with your admin username.
    users = agoAdmin.getUsers()

    outputFile = 'c:/temp/users.csv'

    with open(outputFile, 'wb') as output:
        dataWriter = csv.writer(output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # Write header row.
        dataWriter.writerow(['Full Name', 'Email', 'Username', 'Role', 'Date Created'])
        # Write user data.
        for user in users:
            dataWriter.writerow([user['fullName'], user['email'], user['username'], user['role'], time.strftime("%Y-%m-%d",time.gmtime(user['created']/1000))])

#### Add new users to existing groups
    # Requires admin role.
    import csv, datetime
    from agoTools.admin import Admin

    # User parameters:
    agoAdmin = Admin(<username>)   # Replace <username> with your admin username.
    daysToCheck = 7   # Replace with number of days to check...1 checks past day, 7 checks past week, etc.
    groups = [<groupID1>, <groupID2>, ...]   # Enter <groupIDs> of groups to which you want to add new users
    outputDir = 'c:/temp/'   # Replace with path for report file
	
    outputDate = datetime.datetime.now().strftime("%Y%m%d")   # Current date prefixed to filename.
    outputFile = outputDir + outputDate + '_AddNewUsers2Groups.csv'
	
    userSummary = agoAdmin.addNewUsersToGroups(daysToCheck, groups)
	
    with open(outputFile, 'wb') as output:
        dataWriter = csv.writer(output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # Write header row.
        dataWriter.writerow(['Full Name', 'Email', 'Username', 'Role', 'Date Created'])
        # Write user data.
        for user in userSummary:
            dataWriter.writerow([user['fullName'], user['email'], user['username'], user['role'], time.strftime("%Y-%m-%d", time.gmtime(user['created']/1000))])

#### Move all content from one account to another
    #Requires admin role
	
    from agoTools.admin import Admin
    agoAdmin = Admin(<username>)  #Replace <username> with your admin username
    
    migrateAccount(agoAdmin, <userFrom>, <userTo>)  #Replace with your current and new account usernames
	
#### Move all content between pairs of accounts listed in a CSV

    #Requires admin role
	#Recommend creating CSV in Excel and saving as "CSV (Comma Delimited)"
	
    from agoTools.admin import Admin

    agoAdmin = Admin(<username>)  #Replace <username> with your admin username
    Admin.migrateAccounts(agoAdmin, r'<userMapping.CSV path>')   # Replace <userMapping.CSV path> with path to your file

            
#### Utilities Class
            
#### Update map service urls in webmaps
    from agoTools.utilities import Utilities
    agoUtilities = Utilities(<username>) # Replace <username> with your username.

    webmapId = 'e1d78110b0eg447aab46d373c7360046'
    oldUrl = 'http://myserver.com/arcgis/rest/services/old/MapServer'
    newUrl = 'http://myserver.com/arcgis/rest/services/new/MapServer'

    agoUtilities.updateWebmapService(webmapId, oldUrl, newUrl)
    
#### Update the URL for registered map services or web applications
    from agoTools.utilities import Utilities
    agoUtilities = Utilities(<username>) # Replace <username> with your username.

    itemId = 'e1d78110b0eg447aab46d373c7360046'
    oldUrl = 'http://oldserver.com/app'
    newUrl = 'http://newserver.com/app'

    agoUtilities.updateItemUrl(itemId, oldUrl, newUrl)

#### Move all items from one user to another (within the same Org)
#### Useful when migrating to Enterprise Logins

    from agoTools.admin_working import Admin
	
    myAgol = Admin('<username>')  # Replace <username> your ADMIN account
    Admin.migrateAccount(myAgol, '<userFrom>', '<userTo>')   # Replace with usernames between which you are moving items
	

## Requirements

* Python
* Notepad or your favorite Python editor

## Resources

* [Python for ArcGIS Resource Center](http://resources.arcgis.com/en/communities/python/)
* [ArcGIS Blog](http://blogs.esri.com/esri/arcgis/)
* [twitter@esri](http://twitter.com/esri)

## Issues

Find a bug or want to request a new feature?  Please let us know by submitting an issue.

## Contributing

Anyone and everyone is welcome to contribute. 

## Licensing
Copyright 2013 Esri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

A copy of the license is available in the repository's [license.txt](https://raw.github.com/Esri/ago-tools/master/license.txt) file.

[](Esri Tags: ArcGIS-Online Python Tools Library)
[](Esri Language: Python)
