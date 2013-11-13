#### Search for the top 10 most viewed public items in my organization.

from agoTools import User
import agoTools.utilities

myAgo = User(username=<username>, password=<password>) # replace with your username and password
searchQuery = 'orgid: ' + myAgo.__portalId__()
search = agoTools.utilities.searchPortal(myAgo.portalUrl, query=searchQuery, totalResults=10)

print search
    
    
#### Search for all content owned by a specific user (admin view)

from agoTools.admin import Admin
import agoTools.utilities

myAgo = Admin(username=<username>, password=<password>) # replace with your username and password
search = agoTools.utilities.searchPortal(myAgo.user.portalUrl, query='owner: username', token=myAgo.user.token)

print search
