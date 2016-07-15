### Lists out the admins and members of the first group found by the 
### specified search term.

from agoTools.admin import Admin

username = '<username>'
password = '<password>'
groupSearch = 'Mission Operations'

myAdmin = Admin(username=username, password=password)
groupInfo = myAdmin.findGroup(groupSearch)
groupMembers = myAdmin.getUsersInGroup(groupInfo['id'])

print('Users in {}'.format(groupInfo['title']))
for admin in groupMembers['admins']:
    print('    {} - Admin'.format(admin))
for user in groupMembers['users']:
    print('    {} - Member'.format(user))