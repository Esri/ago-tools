# ago-tools

A Python package to assist with administering ArcGIS Online Organizations.

## Features

* Create a spreadsheet of all users in the org
* Update map service urls in webmaps
* Search for new users and add them to a list of groups
* Move (migrate) all items between accounts (single or batch)
* Search a portal

## Instructions

1. Fork and then clone the repo. 
2. Run and try the samples.

## Installation

1. Unzip into a folder such as C:/myscripts
2. Remove dashes from the directory name (e.g. C:/myscripts/ago-tools-master to C:/myscripts/agoTools)
3. Then do one of the following: A) add that directory to your system path -OR- B) append the directory at runtime using the sys module in python:
      
        import sys
        sys.path.append('c:/myscripts')

## Samples
### Admin Class

* [Create a spreadsheet of all users in the organization](samples/createUserListCSV.py)
* [Add new users to a set of groups](samples/addNewUsersToGroups.py)
* Migrate items and group ownership/membership between user accounts:
  * [Move all items from one account to another, reassign ownership of all groups, and/or add user to another user's groups](samples/moveItemsReassignGroups.py)
  * [Migrate account(s)](samples/migrateAccount.py)
  
### Utilities Class

* [Update map service URLs in web maps](samples/updateMapServiceUrlsInWebMaps.py)
* [Update the URL for registered services or web applications](samples/updateRegisteredUrlForServiceOrApp.py)
* Search Examples:
  * [Search for the top 10 most viewed public items in the organization](samples/searchTopViewedItems.py)
  * [Search for all content owned by a specific user (admin view)](samples/searchAllUserItems.py)
  * [Advanced search examples](search-cheat-sheet.md)


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

Esri welcomes contributions from anyone and everyone. Please see our [guidelines for contributing](https://github.com/esri/contributing).

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
