### This script creates a spreadsheet with key informationa about each user.
### It expands on createUserListCSV.py by adding a field detailing the groups
### each user is a member of.

# Requires admin role.
import csv, time
from agoTools.admin import Admin
from agoTools.utilities import Utilities

username = '<username>'
password = '<password>'
outputFile = 'c:/temp/users.csv'

agoAdmin = Admin(username=username, password=password)
agoUtilities = Utilities(username=username, password=password)

print('Getting users.')
users = agoAdmin.getUsers()
roles = agoAdmin.getRoles()
# Make a dictionary of the roles so we can convert custom roles from their ID to their associated name.
roleLookup = {}
for role in roles:
    roleLookup[role["id"]] = role['name']

# Get the users' groups.
print('Getting each user\'s groups.')
for user in users:
    user['groups'] = []
    groups = agoUtilities.getUserGroups(user['username'])
    for group in groups:
        user['groups'].append(group['title'].encode('utf-8'))

print('Writing the results.')
with open(outputFile, 'wb') as output:
    dataWriter = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Write header row.
    dataWriter.writerow(['Full Name',
                         'Email',
                         'Username',
                         'Role',
                         'Date Created',
                         'Last Login',
                         'Groups'])

    # Write user data.
    for user in users:
        try:
            # Get role name from the id. If it's not in the roles, it's one of the standard roles so just use it.
            roleID = user['role']
            roleName = roleLookup.get(roleID, roleID)
            if user['lastLogin'] > 0:
                lastLogin = time.strftime("%Y-%m-%d", time.gmtime(user['lastLogin']/1000))
            else:
                lastLogin = 'Never'
            dataWriter.writerow([user['fullName'].encode('utf-8'),
                                 user['email'].encode('utf-8'),
                                 user['username'].encode('utf-8'),
                                 roleName,
                                 time.strftime("%Y-%m-%d", time.gmtime(user['created']/1000)),
                                 lastLogin,
                                 ','.join(user['groups'])])
        except:
            print('Problem writing data for {}'.format(user['username']))

print('Finished writing spreadsheet {}'.format(outputFile))
