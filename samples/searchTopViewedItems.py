#### Search for the top 10 most viewed public items in my organization.

from agoTools import User
import agoTools.utilities

myAgo = User(username=<username>, password=<password>) # replace with your username and password
searchQuery = 'orgid: ' + myAgo.__portalId__()
search = agoTools.utilities.searchPortal(myAgo.portalUrl, query=searchQuery, totalResults=10)

print search
