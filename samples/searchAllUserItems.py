#### Search for all content owned by a specific user (admin view)

from agoTools.admin import Admin
import agoTools.utilities

myAgo = Admin(username=<username>, password=<password>) # replace with your username and password
search = agoTools.utilities.searchPortal(myAgo.user.portalUrl, query='owner: username', token=myAgo.user.token)

print search
