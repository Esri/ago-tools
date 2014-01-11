# Requires admin role.
import csv, time, datetime
from agoTools.admin import Admin

# User parameters:
agoAdmin = Admin(<username>)   # Replace <username> with your admin username.
daysToCheck = 7   # Replace with number of days to check...1 checks past day, 7 checks past week, etc.
groups = [<groupID1>, <groupID2>, ...]   # Enter <groupIDs> of groups to which you want to add new users

# Find the group ID with this tool: http://developers.arcgis.com/en/javascript/samples/portal_getgroupamd/
outputDir = 'c:/temp/'   # Replace with path for report file

outputDate = datetime.datetime.now().strftime("%Y%m%d")   # Current date prefixed to filename.
outputFile = outputDir + outputDate + '_AddNewUsers2Groups.csv'

newUsers = agoAdmin.getUsers(daysToCheck=daysToCheck)
groupUsers = []
for user in newUsers:
    groupUsers.append(user['username'])
    
userSummary = agoAdmin.addUsersToGroups(groupUsers, groups)

# print userSummary # Uncomment this line to see a summary of the group additions.
# Reports false-negatives as of Nov 5, 2013.

with open(outputFile, 'wb') as output:
    dataWriter = csv.writer(output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # Write header row.
    dataWriter.writerow(['Full Name', 'Email', 'Username', 'Role', 'Date Created'])
    # Write user data.
    for user in newUsers:
        dataWriter.writerow([user['fullName'], user['email'], user['username'], user['role'], time.strftime("%Y-%m-%d", time.gmtime(user['created']/1000))])