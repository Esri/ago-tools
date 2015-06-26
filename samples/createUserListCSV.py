# Requires admin role.
import csv, time
from agoTools.admin import Admin

agoAdmin = Admin('<username>') # Replace <username> with your admin username.
users = agoAdmin.getUsers()
roles = agoAdmin.getRoles()
#Make a dictionary of the roles so we can convert custom roles from their ID to their associated name.
roleLookup = {}
for role in roles:
    roleLookup[role["id"]] = role["name"]

outputFile = 'c:/temp/users.csv'

with open(outputFile, 'wb') as output:
    dataWriter = csv.writer(output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # Write header row.
    #Groups apparently doesn't work...I'll leave it in so it'll work when it gets implemented. I could make a rest call for each user but that'll take awhile...
    dataWriter.writerow(['Full Name', 'Email', 'Username', 'Role', 'Date Created','Groups'])
    # Write user data.
    for user in users:
        #get role name from the id. If it's not in the roles, it's one of the standard roles so just use it.
        roleID = user['role']
        roleName = roleLookup.get(roleID,roleID)
        dataWriter.writerow([user['fullName'].encode('utf-8'), user['email'].encode('utf-8'), user['username'].encode('utf-8'), roleName, time.strftime("%Y-%m-%d",time.gmtime(user['created']/1000)),",".join(user['groups'])])
