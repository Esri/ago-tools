# ago-tools

A Python package to assist with administering ArcGIS Online Organizations.

## Project Status
>This project is no longer being actively developed. In the short term, the intent is to tidy up any outstanding bugs and small fixes. Longer term, I'd like to rewrite all of the examples from this project to work against the new [ArcGIS API for Python](https://developers.arcgis.com/python/) which will be more robust and ultimately much better maintained than this library. It is actively being developed and you can [join the conversation in the beta](https://earlyadopter.esri.com/callout/?callid={C9060EB8-F000-4611-88F8-4C2D34B28A36}) today. 

>I will continue to accept new PRs in the meantime if anybody is feeling particularly ambitious or wants to help out with the cleanup.

>    @ecaldwell July 7, 2016

## Features

* Create a spreadsheet of all users in the org
* Update map service urls in webmaps
* Search for new users and add them to a list of groups
* Move (migrate) all items between accounts (single or batch)
* Search a portal
* Update sharing of content in groups
* Remove items from an organization
* Automate registration of items via spreadsheet
* Calculate presence of attachments for features

## Installation

1. Download or clone the project.
2. Run `python setup.py install` from the command line **--OR--** add the `agoTools` folder to your script directory.

## Samples
### Admin Class

* [Create a spreadsheet of all users in the organization](samples/createUserListCSV.py)
* [Add new users to a set of groups](samples/addNewUsersToGroups.py)
* Migrate items and group ownership/membership between user accounts:
  * [Move all items from one account to another, reassign ownership of all groups, and/or add user to another user's groups](samples/moveItemsReassignGroups.py)
  * [Migrate account(s)](samples/migrateAccount.py)
* [Generate a CSV listing the items in the organization](samples/AGOLCat.py)
* [Register items listed in an input CSV to the organization](samples/registerItems.py)
* [Remove (delete) all items from a designated folder under My Content](samples/clearFolder.py)
* [Remove (unshare) all items from a designated group in the organization](samples/clearGroup.py)
* [Update any missing thumbnails for items under My Content with a default](samples/updateServiceItemsThumbnail.py)
* [Assign roles to Username and Role from input CSV](samples/updateUserRoles.py)
* [Delete items listed in a CSV from an organization](samples/deleteItems.py)
* [Find items containing reference of specific path](samples/findItemsContainingUrl.py)
* [Insert bookmarks into webmap from feature extents](samples/populateBookmarks.py)
* [Calculate status of attachments for features in layer](samples/flagAttachments.py)


### Utilities Class

* [Update map service URLs in web maps](samples/updateMapServiceUrlsInWebMaps.py)
* [Update the URL for registered services or web applications](samples/updateRegisteredUrlForServiceOrApp.py)
* Search Examples ([search cheat sheet](search-cheat-sheet.md)):
  * [Search for the top 10 most viewed public items in the organization](samples/searchTopViewedItems.py)
  * [Search for all content owned by a specific user (admin view)](samples/searchAllUserItems.py)


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

Please use the following style guides when contributing to this particular repo:

* 4 spaces for indentation
* `'singleQuotes'` instead of `"doubleQuotes"`
* `publicFunction()` vs ` `\_\_internalFunction\_\_()`
* `# Place comments on their own line preceding the code they explain.`


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

A copy of the license is available in the repository's [license.txt](license.txt) file.

[](Esri Tags: ArcGIS-Online Python Tools Library)
[](Esri Language: Python)
