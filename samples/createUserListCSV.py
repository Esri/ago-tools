# Requires admin role.
import csv, time
from agoTools.admin import Admin

agoAdmin = Admin('<username>') # Replace <username> with your admin username.
outputFile = 'c:/temp/users.csv'

users = agoAdmin.getUsers()
roles = agoAdmin.getRoles()

#Make a dictionary of the roles so we can convert custom roles from their ID to their associated name.
roleLookup = {}
for role in roles:
    roleLookup[role["id"]] = role["name"]

with open(outputFile, 'wb') as output:
    dataWriter = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Write header row.
    dataWriter.writerow(['Full Name',
                         'Email',
                         'Username',
                         'Role',
                         'Date Created'])
    # Write user data.
    for user in users:
        #get role name from the id. If it's not in the roles, it's one of the standard roles so just use it.
        roleID = user['role']
        roleName = roleLookup.get(roleID,roleID)
        dataWriter.writerow([user['fullName'].encode('utf-8'),
                             user['email'].encode('utf-8'),
                             user['username'].encode('utf-8'),
                             roleName,
                             time.strftime("%Y-%m-%d",time.gmtime(user['created']/1000))])
        
print('Finished writing spreadsheet {}'.format(outputFile))
